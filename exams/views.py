from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from accounts.permissions import role_required
from subjects.models import Subject
from questions.models import Question
from questions.services import QuestionService
from .models import Exam, ExamAttempt, AttemptViolation
from .forms import ExamConfigForm, ExamEntryForm
from .services import ExamService

@login_required
def exam_list_view(request):
    if request.user.role == 'TEACHER':
        exams = Exam.objects.filter(subject__assigned_teacher=request.user).select_related('subject')
    elif request.user.role == 'STUDENT':
        return redirect('student_upcoming_exams')
    else:
        exams = Exam.objects.select_related('subject').all()

    return render(request, 'exams/exam_list.html', {'exams': exams})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def exam_create_view(request):
    subjects = Subject.objects.filter(assigned_teacher=request.user) if request.user.role == 'TEACHER' else Subject.objects.all()
    if request.method == 'POST':
        form = ExamConfigForm(request.POST, request.FILES)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()

            # Process questions addition (PDF import or random sampler)
            pdf_file = request.FILES.get('question_pdf')
            if pdf_file:
                imported_questions = QuestionService.import_questions_from_pdf(pdf_file, exam.subject)
                exam.questions.set(imported_questions)
                messages.success(request, f"Exam '{exam.title}' configured with {imported_questions.count()} questions extracted from PDF!")
            else:
                num_questions = int(request.POST.get('num_questions', 20))
                sampled_questions = QuestionService.generate_random_questions(exam.subject.id, num_questions)
                exam.questions.set(sampled_questions)
                messages.success(request, f"Exam '{exam.title}' configured with {sampled_questions.count()} questions!")

            return redirect('exam_list')
    else:
        form = ExamConfigForm()
        if request.user.role == 'TEACHER':
            form.fields['subject'].queryset = subjects

    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Create New Exam'})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def exam_edit_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamConfigForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated successfully!")
            return redirect('exam_list')
    else:
        form = ExamConfigForm(instance=exam)

    return render(request, 'exams/exam_form.html', {'form': form, 'exam': exam, 'title': 'Edit Exam'})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def exam_delete_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, "Exam deleted successfully!")
        return redirect('exam_list')
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})

@login_required
@role_required(['STUDENT'])
def student_upcoming_exams_view(request):
    now = timezone.now()
    active_exams = Exam.objects.filter(is_published=True, start_time__lte=now, end_time__gte=now).select_related('subject')
    upcoming_exams = Exam.objects.filter(is_published=True, start_time__gt=now).select_related('subject')
    
    # User's attempts
    attempts = ExamAttempt.objects.filter(student=request.user).select_related('exam')
    attempted_exam_ids = set(attempts.values_list('exam_id', flat=True))

    return render(request, 'exams/student_upcoming.html', {
        'active_exams': active_exams,
        'upcoming_exams': upcoming_exams,
        'attempted_exam_ids': attempted_exam_ids,
        'attempts': attempts
    })

@login_required
@role_required(['STUDENT'])
def exam_instructions_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk, is_published=True)
    if request.method == 'POST':
        form = ExamEntryForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data.get('password')
            if exam.password and passcode != exam.password:
                messages.error(request, "Incorrect exam passcode.")
            else:
                attempt = ExamService.start_exam_attempt(request.user, exam)
                return redirect('start_exam', attempt_id=attempt.id)
    else:
        form = ExamEntryForm()

    return render(request, 'exams/exam_instructions.html', {
        'exam': exam,
        'form': form
    })

@login_required
@role_required(['STUDENT'])
def start_exam_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    
    # Check if time expired or disqualified
    remaining_sec = ExamService.get_remaining_seconds(attempt)
    if remaining_sec <= 0 or attempt.status in [ExamAttempt.Status.COMPLETED, ExamAttempt.Status.DISQUALIFIED]:
        if attempt.status == ExamAttempt.Status.IN_PROGRESS:
            attempt.status = ExamAttempt.Status.TIMED_OUT
            attempt.end_time = timezone.now()
            attempt.save(update_fields=['status', 'end_time'])
            from results.services import GradingService
            GradingService.evaluate_attempt(attempt)
        return redirect('result_detail', attempt_id=attempt.id)

    # Fetch ordered questions
    question_ids = attempt.question_order
    questions_dict = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
    ordered_questions = [questions_dict[qid] for qid in question_ids if qid in questions_dict]

    # Fetch existing answers saved for this attempt
    from results.models import AnswerAttempt
    saved_answers = {a.question_id: a for a in AnswerAttempt.objects.filter(attempt=attempt)}

    return render(request, 'exams/exam_taking.html', {
        'attempt': attempt,
        'exam': attempt.exam,
        'questions': ordered_questions,
        'saved_answers': saved_answers,
        'remaining_seconds': remaining_sec
    })

@login_required
@require_POST
def autosave_answer_ajax(request):
    attempt_id = request.POST.get('attempt_id')
    question_id = request.POST.get('question_id')
    selected_option = request.POST.get('selected_option', '')
    text_response = request.POST.get('text_response', '')
    is_marked_review = request.POST.get('marked_for_review') == 'true'

    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    if attempt.status != ExamAttempt.Status.IN_PROGRESS:
        return JsonResponse({'status': 'error', 'message': 'Exam attempt is no longer active'}, status=400)

    from results.models import AnswerAttempt
    answer, created = AnswerAttempt.objects.get_or_create(
        attempt=attempt,
        question_id=question_id,
        defaults={
            'selected_option': selected_option,
            'text_response': text_response,
            'is_marked_for_review': is_marked_review
        }
    )
    if not created:
        answer.selected_option = selected_option
        answer.text_response = text_response
        answer.is_marked_for_review = is_marked_review
        answer.save()

    return JsonResponse({'status': 'saved', 'question_id': question_id})

@login_required
@require_POST
def log_violation_ajax(request):
    attempt_id = request.POST.get('attempt_id')
    v_type = request.POST.get('violation_type', AttemptViolation.Type.TAB_SWITCH)
    details = request.POST.get('details', '')

    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    if attempt.status != ExamAttempt.Status.IN_PROGRESS:
        return JsonResponse({'disqualified': True})

    disqualified = ExamService.log_violation(attempt, v_type, details)
    return JsonResponse({
        'status': 'logged',
        'violations_count': attempt.violations_count,
        'max_allowed': attempt.exam.max_violations,
        'disqualified': disqualified
    })

@login_required
@require_POST
def submit_exam_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    if attempt.status == ExamAttempt.Status.IN_PROGRESS:
        attempt.status = ExamAttempt.Status.COMPLETED
        attempt.end_time = timezone.now()
        attempt.save(update_fields=['status', 'end_time'])

        from results.services import GradingService
        GradingService.evaluate_attempt(attempt)
        messages.success(request, "Exam submitted successfully!")

    return redirect('result_detail', attempt_id=attempt.id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from accounts.permissions import role_required
from exams.models import ExamAttempt, Exam
from exams.utils import calculate_grade
from questions.models import Question
from .models import AnswerAttempt
from .services import ResultPDFService, GradingService

@login_required
def result_detail_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt.objects.select_related('exam', 'student', 'exam__subject'), id=attempt_id)
    
    # Permission check: Student can view own result, Teacher/Admin can view all
    if request.user.role == 'STUDENT' and attempt.student != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    # Fetch ordered questions from the attempt's saved sequence
    question_ids = attempt.question_order
    questions_dict = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
    ordered_questions = [questions_dict[qid] for qid in question_ids if qid in questions_dict]
    saved_answers = {a.question_id: a for a in AnswerAttempt.objects.filter(attempt=attempt).select_related('question')}

    # Calculate scale factor to match exam total_marks (using all exam questions)
    base_marks_sum = sum(float(q.marks) for q in ordered_questions)
    exam_total = float(attempt.exam.total_marks) if float(attempt.exam.total_marks) > 0.0 else 100.0
    scale_factor = exam_total / base_marks_sum if base_marks_sum > 0.0 else 1.0

    answers = []
    correct_count = 0
    wrong_count = 0
    skipped_count = 0

    for q in ordered_questions:
        ans = saved_answers.get(q.id)
        if not ans:
            # Create a dummy in-memory AnswerAttempt for rendering skipped questions
            ans = AnswerAttempt(
                attempt=attempt,
                question=q,
                selected_option='',
                text_response='',
                marks_obtained=0.0,
                is_correct=False
            )
            skipped_count += 1
        else:
            if ans.is_correct:
                correct_count += 1
            elif ans.selected_option or ans.text_response:
                wrong_count += 1
            else:
                skipped_count += 1
                
        ans.scaled_max_marks = round(float(q.marks) * scale_factor, 2)
        answers.append(ans)
    
    grade = calculate_grade(attempt.percentage)
    
    # Calculate rank among all evaluated attempts for this exam
    rank = ExamAttempt.objects.filter(exam=attempt.exam, is_evaluated=True, total_score__gt=attempt.total_score).count() + 1

    time_taken_min = 0
    if attempt.end_time and attempt.start_time:
        time_taken_min = round((attempt.end_time - attempt.start_time).total_seconds() / 60, 1)

    # Fetch AI study planner details
    from analytics.services import AIStudyPlannerService
    planner_data = AIStudyPlannerService.get_planner_data(request.user)

    return render(request, 'results/result_detail.html', {
        'attempt': attempt,
        'exam': attempt.exam,
        'answers': answers,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'skipped_count': skipped_count,
        'grade': grade,
        'rank': rank,
        'time_taken_min': time_taken_min,
        'planner_data': planner_data
    })

@login_required
def download_result_pdf_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)
    if request.user.role == 'STUDENT' and attempt.student != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    return ResultPDFService.generate_result_pdf(attempt)

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def teacher_manual_grading_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt.objects.select_related('exam', 'student'), id=attempt_id)
    answers = list(AnswerAttempt.objects.filter(attempt=attempt).select_related('question'))
    
    # Calculate scale factor
    base_marks_sum = sum(float(q.marks) for q in attempt.exam.questions.all())
    exam_total = float(attempt.exam.total_marks) if float(attempt.exam.total_marks) > 0.0 else 100.0
    scale_factor = exam_total / base_marks_sum if base_marks_sum > 0.0 else 1.0
    
    for ans in answers:
        ans.scaled_max_marks = round(float(ans.question.marks) * scale_factor, 2)

    return render(request, 'results/manual_grading.html', {
        'attempt': attempt,
        'answers': answers
    })

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
@require_POST
def save_manual_grade_ajax(request):
    answer_id = request.POST.get('answer_id')
    marks = request.POST.get('marks')
    feedback = request.POST.get('feedback', '')

    ans = get_object_or_404(AnswerAttempt, id=answer_id)
    ans.marks_obtained = float(marks)
    ans.is_correct = ans.marks_obtained > 0
    ans.teacher_feedback = feedback
    ans.evaluated_by = request.user
    ans.save()

    # Recalculate total score for attempt
    attempt = ans.attempt
    total_score = sum([float(a.marks_obtained) for a in attempt.answers.all()])
    attempt.total_score = max(0.0, total_score)
    
    total_possible = float(attempt.exam.total_marks) if float(attempt.exam.total_marks) > 0 else 100.0
    attempt.percentage = round((attempt.total_score / total_possible) * 100.0, 2)
    attempt.is_passed = attempt.total_score >= float(attempt.exam.passing_marks)
    attempt.save(update_fields=['total_score', 'percentage', 'is_passed'])

    return JsonResponse({
        'status': 'success',
        'new_total_score': attempt.total_score,
        'percentage': attempt.percentage
    })

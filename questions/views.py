from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from accounts.permissions import role_required
from subjects.models import Subject
from .models import Question
from .forms import QuestionForm, QuestionExcelImportForm
from .services import QuestionService

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def question_list_view(request):
    subject_id = request.GET.get('subject')
    difficulty = request.GET.get('difficulty')
    q_type = request.GET.get('type')
    search_query = request.GET.get('q')

    questions = Question.objects.select_related('subject').all()
    if request.user.role == 'TEACHER':
        questions = questions.filter(subject__assigned_teacher=request.user)

    if subject_id:
        questions = questions.filter(subject_id=subject_id)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    if q_type:
        questions = questions.filter(question_type=q_type)
    if search_query:
        questions = questions.filter(prompt_text__icontains=search_query)

    subjects = Subject.objects.filter(assigned_teacher=request.user) if request.user.role == 'TEACHER' else Subject.objects.all()

    return render(request, 'questions/question_list.html', {
        'questions': questions,
        'subjects': subjects,
        'selected_subject': subject_id,
        'selected_difficulty': difficulty,
        'selected_type': q_type,
        'search_query': search_query
    })

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def question_create_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            messages.success(request, "Question added to Question Bank!")
            return redirect('question_list')
    else:
        form = QuestionForm()
        if request.user.role == 'TEACHER':
            form.fields['subject'].queryset = Subject.objects.filter(assigned_teacher=request.user)

    return render(request, 'questions/question_form.html', {'form': form, 'title': 'Add New Question'})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def question_edit_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
        if request.user.role == 'TEACHER':
            form.fields['subject'].queryset = Subject.objects.filter(assigned_teacher=request.user)

    return render(request, 'questions/question_form.html', {'form': form, 'title': 'Edit Question', 'question': question})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def question_delete_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question removed from Question Bank!")
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def question_export_excel_view(request):
    subject_id = request.GET.get('subject')
    return QuestionService.export_questions_to_excel(subject_id)

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def question_import_excel_view(request):
    subjects = Subject.objects.filter(assigned_teacher=request.user) if request.user.role == 'TEACHER' else Subject.objects.all()
    if request.method == 'POST':
        form = QuestionExcelImportForm(request.POST, request.FILES, subjects=subjects)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            subject_obj = form.cleaned_data['subject']
            count = QuestionService.import_questions_from_excel(excel_file, subject_obj)
            messages.success(request, f"Successfully imported {count} questions for {subject_obj.name}!")
            return redirect('question_list')
    else:
        form = QuestionExcelImportForm(subjects=subjects)
    return render(request, 'questions/question_import.html', {'form': form})

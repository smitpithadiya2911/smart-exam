from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from .models import Subject
from .forms import SubjectForm

@login_required
def subject_list_view(request):
    if request.user.role == 'TEACHER':
        subjects = Subject.objects.filter(assigned_teacher=request.user).select_related('semester', 'assigned_teacher')
    else:
        subjects = Subject.objects.select_related('semester', 'assigned_teacher').all()
        
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Subject created successfully!")
        return redirect('subject_list')
        
    return render(request, 'subjects/subject_list.html', {
        'subjects': subjects,
        'form': form
    })

@login_required
@role_required(['SUPER_ADMIN'])
def subject_edit_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Subject updated successfully!")
        return redirect('subject_list')
    return render(request, 'subjects/subject_edit.html', {'form': form, 'subject': subject})

@login_required
@role_required(['SUPER_ADMIN'])
def subject_delete_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect('subject_list')
    return render(request, 'subjects/subject_confirm_delete.html', {'subject': subject})

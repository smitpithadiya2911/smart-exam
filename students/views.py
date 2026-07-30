from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from accounts.models import User
from .models import StudentProfile
from .forms import StudentProfileForm, StudentEditForm

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def student_list_view(request):
    students = StudentProfile.objects.select_related('user', 'department', 'course', 'semester').all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def student_edit_view(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    user = profile.user
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=profile)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save(update_fields=['first_name', 'last_name', 'email'])
            form.save()
            messages.success(request, f"Student profile for {user.get_full_name()} updated successfully!")
            return redirect('student_list')
    else:
        form = StudentEditForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })

    return render(request, 'students/student_edit.html', {'form': form, 'student': profile})

@login_required
@role_required(['SUPER_ADMIN'])
def student_delete_view(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    user = profile.user
    if request.method == 'POST':
        user.delete() # Deletes user & profile
        messages.success(request, "Student account deleted successfully!")
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': profile})

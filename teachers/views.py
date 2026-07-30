from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from accounts.models import User
from .models import TeacherProfile
from .forms import TeacherRegistrationForm, TeacherEditForm

@login_required
@role_required(['SUPER_ADMIN'])
def teacher_list_view(request):
    teachers = TeacherProfile.objects.select_related('user', 'department').all()
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.TEACHER
            )
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, f"Teacher account for Prof. {user.get_full_name()} created successfully!")
            return redirect('teacher_list')
    else:
        form = TeacherRegistrationForm()

    return render(request, 'teachers/teacher_list.html', {
        'teachers': teachers,
        'form': form
    })

@login_required
@role_required(['SUPER_ADMIN'])
def teacher_edit_view(request, pk):
    profile = get_object_or_404(TeacherProfile, pk=pk)
    user = profile.user
    if request.method == 'POST':
        form = TeacherEditForm(request.POST, instance=profile)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save(update_fields=['first_name', 'last_name', 'email'])
            form.save()
            messages.success(request, f"Teacher account for Prof. {user.get_full_name()} updated successfully!")
            return redirect('teacher_list')
    else:
        form = TeacherEditForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })

    return render(request, 'teachers/teacher_edit.html', {'form': form, 'teacher': profile})

@login_required
@role_required(['SUPER_ADMIN'])
def teacher_delete_view(request, pk):
    profile = get_object_or_404(TeacherProfile, pk=pk)
    user = profile.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Teacher account deleted successfully!")
        return redirect('teacher_list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': profile})

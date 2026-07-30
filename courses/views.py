from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from .models import Course
from .forms import CourseForm

@login_required
@role_required(['SUPER_ADMIN'])
def course_list_view(request):
    courses = Course.objects.select_related('department').all()
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Course created successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'form': form
    })

@login_required
@role_required(['SUPER_ADMIN'])
def course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Course updated successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_edit.html', {'form': form, 'course': course})

@login_required
@role_required(['SUPER_ADMIN'])
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from .models import Semester
from .forms import SemesterForm

@login_required
@role_required(['SUPER_ADMIN'])
def semester_list_view(request):
    semesters = Semester.objects.select_related('course').all()
    form = SemesterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Semester added successfully!")
        return redirect('semester_list')
    return render(request, 'semesters/semester_list.html', {
        'semesters': semesters,
        'form': form
    })

@login_required
@role_required(['SUPER_ADMIN'])
def semester_edit_view(request, pk):
    sem = get_object_or_404(Semester, pk=pk)
    form = SemesterForm(request.POST or None, instance=sem)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Semester updated successfully!")
        return redirect('semester_list')
    return render(request, 'semesters/semester_edit.html', {'form': form, 'semester': sem})

@login_required
@role_required(['SUPER_ADMIN'])
def semester_delete_view(request, pk):
    sem = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        sem.delete()
        messages.success(request, "Semester deleted successfully!")
        return redirect('semester_list')
    return render(request, 'semesters/semester_confirm_delete.html', {'semester': sem})

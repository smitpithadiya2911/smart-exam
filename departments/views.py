from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from .models import Department
from .forms import DepartmentForm

@login_required
@role_required(['SUPER_ADMIN'])
def department_list_view(request):
    departments = Department.objects.all()
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Department added successfully!")
        return redirect('department_list')
    return render(request, 'departments/department_list.html', {
        'departments': departments,
        'form': form
    })

@login_required
@role_required(['SUPER_ADMIN'])
def department_edit_view(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Department updated successfully!")
        return redirect('department_list')
    return render(request, 'departments/department_edit.html', {
        'form': form,
        'department': dept
    })

@login_required
@role_required(['SUPER_ADMIN'])
def department_delete_view(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')
    return render(request, 'departments/department_confirm_delete.html', {'department': dept})

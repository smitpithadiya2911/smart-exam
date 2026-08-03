import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import StudyMaterial, MaterialDownloadHistory
from .forms import StudyMaterialForm

def is_management(user):
    return user.role in ['ADMIN', 'SUPER_ADMIN', 'TEACHER'] or user.is_superuser

# --- Admin / Teacher Views ---

@login_required
def material_manage_list(request):
    if not is_management(request.user):
        messages.error(request, "Access Denied. You do not have permission to manage study materials.")
        return redirect('dashboard')
        
    query = request.GET.get('q', '')
    materials = StudyMaterial.objects.all()
    
    # Teachers see only their own, unless admin
    if request.user.role == 'TEACHER':
        materials = materials.filter(uploaded_by=request.user)
        
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
        
    paginator = Paginator(materials, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'study_materials/material_list_admin.html', {
        'page_obj': page_obj,
        'query': query
    })

@login_required
def material_create(request):
    if not is_management(request.user):
        messages.error(request, "Access Denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            messages.success(request, "Study material uploaded successfully!")
            return redirect('material_manage_list')
    else:
        form = StudyMaterialForm()
        
    return render(request, 'study_materials/material_form.html', {'form': form, 'title': 'Upload Study Material'})

@login_required
def material_update(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    if not is_management(request.user) or (request.user.role == 'TEACHER' and material.uploaded_by != request.user):
        messages.error(request, "Access Denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, "Study material updated successfully!")
            return redirect('material_manage_list')
    else:
        form = StudyMaterialForm(instance=material)
        
    return render(request, 'study_materials/material_form.html', {'form': form, 'title': 'Edit Study Material'})

@login_required
def material_delete(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    if not is_management(request.user) or (request.user.role == 'TEACHER' and material.uploaded_by != request.user):
        messages.error(request, "Access Denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        material.delete()
        messages.success(request, "Study material deleted successfully!")
        return redirect('material_manage_list')
        
    return render(request, 'study_materials/material_confirm_delete.html', {'material': material})


# --- Student Views ---

@login_required
def student_material_list(request):
    if request.user.role != 'STUDENT':
        return redirect('material_manage_list')
        
    # Get materials visible to this student based on course/semester
    student = request.user.student_profile
    materials = StudyMaterial.objects.filter(
        Q(visibility='ALL') |
        Q(visibility='COURSE', course=student.course) |
        Q(visibility='SEMESTER', semester=student.semester) |
        Q(visibility='SUBJECT', subject__in=student.course.subjects.all() if student.course else [])
    ).distinct()

    query = request.GET.get('q', '')
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
        
    paginator = Paginator(materials, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'study_materials/material_list_student.html', {
        'page_obj': page_obj,
        'query': query
    })

@login_required
def material_detail(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    # Check permissions if student
    if request.user.role == 'STUDENT':
        student = request.user.student_profile
        has_access = (
            material.visibility == 'ALL' or
            (material.visibility == 'COURSE' and material.course == student.course) or
            (material.visibility == 'SEMESTER' and material.semester == student.semester) or
            (material.visibility == 'SUBJECT' and material.subject in (student.course.subjects.all() if student.course else []))
        )
        if not has_access:
            messages.error(request, "You do not have access to this material.")
            return redirect('student_material_list')
            
    return render(request, 'study_materials/material_detail.html', {'material': material})

@login_required
def material_download(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    if request.user.role == 'STUDENT':
        # Verify access
        student = request.user.student_profile
        has_access = (
            material.visibility == 'ALL' or
            (material.visibility == 'COURSE' and material.course == student.course) or
            (material.visibility == 'SEMESTER' and material.semester == student.semester) or
            (material.visibility == 'SUBJECT' and material.subject in (student.course.subjects.all() if student.course else []))
        )
        if not has_access:
            raise Http404("Material not found or access denied.")
            
        # Record download history
        MaterialDownloadHistory.objects.create(
            student=request.user,
            material=material,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
    if not material.file:
        raise Http404("File missing.")
        
    try:
        file_path = material.file.path
        if not os.path.exists(file_path):
            raise Http404("File not found on server.")
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        return response
    except Exception:
        raise Http404("Could not serve file.")

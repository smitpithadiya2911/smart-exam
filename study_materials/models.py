import os
from django.db import models
from django.conf import settings
from subjects.models import Subject
from courses.models import Course
from semesters.models import Semester
from departments.models import Department

def study_material_upload_path(instance, filename):
    # e.g., media/study_materials/pdf/filename.pdf
    ext = filename.split('.')[-1].lower()
    folder = 'other'
    if ext in ['pdf']:
        folder = 'pdf'
    elif ext in ['doc', 'docx']:
        folder = 'docx'
    elif ext in ['ppt', 'pptx']:
        folder = 'ppt'
    elif ext in ['xls', 'xlsx']:
        folder = 'xlsx'
    elif ext in ['jpg', 'jpeg', 'png', 'gif']:
        folder = 'images'
    elif ext in ['mp4', 'mkv', 'avi']:
        folder = 'videos'
    elif ext in ['zip', 'rar']:
        folder = 'archives'
        
    return os.path.join('study_materials', folder, filename)

class StudyMaterial(models.Model):
    MATERIAL_TYPES = [
        ('PDF', 'PDF Document'),
        ('DOCX', 'Word Document'),
        ('PPT', 'PowerPoint'),
        ('XLSX', 'Excel Spreadsheet'),
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('ZIP', 'ZIP Archive'),
        ('OTHER', 'Other'),
    ]

    VISIBILITY_CHOICES = [
        ('ALL', 'All Students'),
        ('COURSE', 'Specific Course'),
        ('SEMESTER', 'Specific Semester'),
        ('SUBJECT', 'Specific Subject'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Relationships
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_materials')
    
    # File details
    file = models.FileField(upload_to=study_material_upload_path)
    thumbnail = models.ImageField(upload_to='study_materials/thumbnails/', blank=True, null=True)
    
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES, default='OTHER')
    visibility = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default='ALL')
    
    upload_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return self.title

    @property
    def download_count(self):
        return self.downloads.count()

class MaterialDownloadHistory(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='material_downloads')
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='downloads')
    download_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-download_date']

    def __str__(self):
        return f"{self.student.get_full_name() or self.student.email} downloaded {self.material.title}"

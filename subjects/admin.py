from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'semester', 'assigned_teacher', 'credits')
    list_filter = ('semester__course', 'semester')
    search_fields = ('name', 'code')

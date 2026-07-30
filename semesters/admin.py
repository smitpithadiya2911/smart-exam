from django.contrib import admin
from .models import Semester

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'name', 'start_date', 'end_date', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('name', 'course__name')

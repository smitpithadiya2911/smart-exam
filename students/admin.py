from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'course', 'semester')
    list_filter = ('department', 'course', 'semester')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'roll_number')

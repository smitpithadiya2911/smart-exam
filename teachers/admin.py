from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'designation')
    list_filter = ('department', 'designation')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'employee_id')

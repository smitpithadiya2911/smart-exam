from django.contrib import admin
from .models import Exam, ExamAttempt, AttemptViolation

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'start_time', 'end_time', 'duration_minutes', 'is_published')
    list_filter = ('subject', 'is_published')
    search_fields = ('title', 'subject__name')

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'status', 'total_score', 'cheating_detected', 'auto_submitted', 'start_time')
    list_filter = ('status', 'is_passed', 'cheating_detected', 'auto_submitted')
    search_fields = ('student__email', 'exam__title')
    readonly_fields = ('cheating_detected', 'auto_submitted', 'failure_reason')

@admin.register(AttemptViolation)
class AttemptViolationAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'violation_type', 'timestamp')
    list_filter = ('violation_type', 'timestamp')

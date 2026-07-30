from django.contrib import admin
from .models import AnswerAttempt

@admin.register(AnswerAttempt)
class AnswerAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'marks_obtained')
    list_filter = ('is_correct', 'is_marked_for_review')

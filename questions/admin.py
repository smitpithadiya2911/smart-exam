from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('prompt_snippet', 'subject', 'question_type', 'difficulty', 'marks', 'created_at')
    list_filter = ('subject', 'question_type', 'difficulty')
    search_fields = ('prompt_text', 'chapter', 'topic', 'tags')

    def prompt_snippet(self, obj):
        return obj.prompt_text[:50]
    prompt_snippet.short_description = 'Question'

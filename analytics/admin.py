from django.contrib import admin
from .models import AIStudyRecommendation

@admin.register(AIStudyRecommendation)
class AIStudyRecommendationAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject_name', 'weak_topic', 'accuracy_percentage', 'created_at')
    list_filter = ('subject_name', 'created_at')
    search_fields = ('student__email', 'weak_topic')

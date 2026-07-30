from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'rating', 'is_approved', 'created_at')
    list_filter = ('feedback_type', 'is_approved', 'rating')
    search_fields = ('user__email', 'comments')

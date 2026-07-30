from django.db import models
from django.conf import settings
from exams.models import Exam

class Feedback(models.Model):
    class Type(models.TextChoices):
        SYSTEM = 'SYSTEM', 'System / Platform Feedback'
        TEACHER = 'TEACHER', 'Teacher / Course Feedback'
        EXAM = 'EXAM', 'Exam Feedback'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=Type.choices, default=Type.SYSTEM)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5 stars")
    comments = models.TextField()
    is_approved = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} | Rating: {self.rating}/5 | {self.get_feedback_type_display()}"

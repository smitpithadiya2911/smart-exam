from django.db import models
from django.conf import settings

class AIStudyRecommendation(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_recommendations')
    subject_name = models.CharField(max_length=150)
    weak_topic = models.CharField(max_length=150)
    accuracy_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    recommendation_text = models.TextField()
    suggested_chapter = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.email} - Weak Topic: {self.weak_topic} ({self.accuracy_percentage}%)"

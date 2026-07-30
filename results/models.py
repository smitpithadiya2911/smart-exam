from django.db import models
from django.conf import settings
from exams.models import ExamAttempt
from questions.models import Question

class AnswerAttempt(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    
    selected_option = models.CharField(max_length=500, blank=True, null=True, help_text="e.g. A, B, True, etc.")
    text_response = models.TextField(blank=True, null=True, help_text="Subjective or coding text response")
    is_marked_for_review = models.BooleanField(default=False)
    
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_correct = models.BooleanField(default=False)
    
    teacher_feedback = models.TextField(blank=True, null=True)
    evaluated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluated_answers'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('attempt', 'question')
        verbose_name = 'Answer Attempt'
        verbose_name_plural = 'Answer Attempts'

    def __str__(self):
        return f"Attempt {self.attempt.id} | Q: {self.question.id} | Marks: {self.marks_obtained}"

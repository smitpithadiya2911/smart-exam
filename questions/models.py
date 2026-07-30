from django.db import models
from subjects.models import Subject

class Question(models.Model):
    class Type(models.TextChoices):
        MCQ = 'MCQ', 'Multiple Choice'
        TRUE_FALSE = 'TF', 'True / False'
        FILL_BLANK = 'FILL', 'Fill in the Blank'
        SHORT = 'SHORT', 'Short Answer'
        LONG = 'LONG', 'Long Answer'
        CODING = 'CODING', 'Coding Problem'

    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Easy'
        MEDIUM = 'MEDIUM', 'Medium'
        HARD = 'HARD', 'Hard'

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=Type.choices, default=Type.MCQ, db_index=True)
    chapter = models.CharField(max_length=150, blank=True, null=True)
    topic = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM, db_index=True)
    
    prompt_text = models.TextField(help_text="Question text or statement")
    
    # Options for MCQ
    option_a = models.CharField(max_length=500, blank=True, null=True)
    option_b = models.CharField(max_length=500, blank=True, null=True)
    option_c = models.CharField(max_length=500, blank=True, null=True)
    option_d = models.CharField(max_length=500, blank=True, null=True)
    
    correct_answer = models.TextField(help_text="For MCQ: A/B/C/D. For T/F: True/False. For Fill/Short: exact answer.")
    explanation = models.TextField(blank=True, null=True, help_text="Solution explanation for student result review")
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['subject', '-created_at']
        indexes = [
            models.Index(fields=['subject', 'difficulty', 'question_type']),
        ]
        verbose_name = 'Question'
        verbose_name_plural = 'Question Bank'

    def __str__(self):
        return f"[{self.subject.code}] [{self.get_question_type_display()}] {self.prompt_text[:60]}"

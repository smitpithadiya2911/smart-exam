from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from subjects.models import Subject
from questions.models import Question

class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_exams')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=100.0)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, default=40.0)
    negative_marking = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, help_text="Negative marks per wrong objective answer e.g. 0.25")
    
    shuffle_questions = models.BooleanField(default=True)
    shuffle_options = models.BooleanField(default=True)
    attempt_limit = models.PositiveIntegerField(default=1)
    password = models.CharField(max_length=50, blank=True, null=True, help_text="Optional passcode for exam entry")
    instructions = models.TextField(default="Read all questions carefully. Do not switch tabs or exit full-screen mode during the exam.")
    
    is_published = models.BooleanField(default=False)
    max_violations = models.PositiveIntegerField(default=3, help_text="Auto-submit exam after this number of anti-cheat violations")

    questions = models.ManyToManyField(Question, related_name='exams', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']
        constraints = [
            models.CheckConstraint(
                check=models.Q(passing_marks__lte=models.F('total_marks')),
                name='exam_passing_marks_lte_total'
            )
        ]
        indexes = [
            models.Index(fields=['is_published', 'start_time', 'end_time']),
        ]
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def clean(self):
        if self.passing_marks and self.total_marks and self.passing_marks > self.total_marks:
            raise ValidationError({'passing_marks': 'Passing marks cannot exceed total marks.'})
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({'end_time': 'End time must be strictly after start time.'})

    @property
    def is_upcoming(self):
        return timezone.now() < self.start_time

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time and self.is_published

    @property
    def is_expired(self):
        return timezone.now() > self.end_time

    def __str__(self):
        return f"{self.title} ({self.subject.code})"

class ExamAttempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        TIMED_OUT = 'TIMED_OUT', 'Timed Out'
        DISQUALIFIED = 'DISQUALIFIED', 'Disqualified (Violations)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_attempts')
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS, db_index=True)
    
    total_score = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_passed = models.BooleanField(default=False)
    
    violations_count = models.PositiveIntegerField(default=0)
    is_evaluated = models.BooleanField(default=False)
    
    cheating_detected = models.BooleanField(default=False)
    auto_submitted = models.BooleanField(default=False)
    failure_reason = models.TextField(blank=True, null=True)

    # Order of question IDs served to this student (for shuffle consistency)
    question_order = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Exam Attempt'
        verbose_name_plural = 'Exam Attempts'

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam.title} ({self.get_status_display()})"

class AttemptViolation(models.Model):
    class Type(models.TextChoices):
        TAB_SWITCH = 'TAB_SWITCH', 'Tab Switch'
        WINDOW_BLUR = 'WINDOW_BLUR', 'Window Blur / Focus Lost'
        FULLSCREEN_EXIT = 'FULLSCREEN_EXIT', 'Exited Full Screen'
        COPY_PASTE = 'COPY_PASTE', 'Copy / Paste Attempt'
        REFRESH = 'REFRESH', 'Page Refresh'

    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=20, choices=Type.choices)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.get_violation_type_display()}] on Attempt {self.attempt.id} at {self.timestamp.strftime('%H:%M:%S')}"

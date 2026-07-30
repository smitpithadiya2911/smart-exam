from django.db import models
from django.conf import settings

class Notification(models.Model):
    class Type(models.TextChoices):
        EXAM_ALERT = 'EXAM_ALERT', 'Exam Schedule Alert'
        RESULT_PUBLISHED = 'RESULT_PUBLISHED', 'Result Published'
        CERTIFICATE_ISSUED = 'CERTIFICATE_ISSUED', 'Certificate Awarded'
        ANNOUNCEMENT = 'ANNOUNCEMENT', 'Admin Announcement'

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False, db_index=True)
    notification_type = models.CharField(max_length=30, choices=Type.choices, default=Type.ANNOUNCEMENT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.email} | {self.title} ({'Read' if self.is_read else 'Unread'})"

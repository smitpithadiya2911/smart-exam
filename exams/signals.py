from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ExamAttempt

@receiver(post_save, sender=ExamAttempt)
def attempt_saved_signal(sender, instance, created, **kwargs):
    pass

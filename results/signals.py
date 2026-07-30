from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AnswerAttempt

@receiver(post_save, sender=AnswerAttempt)
def answer_saved_signal(sender, instance, created, **kwargs):
    pass

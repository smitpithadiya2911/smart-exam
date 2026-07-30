from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question

@receiver(post_save, sender=Question)
def question_saved_signal(sender, instance, created, **kwargs):
    pass

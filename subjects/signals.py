from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subject

@receiver(post_save, sender=Subject)
def subject_saved_signal(sender, instance, created, **kwargs):
    pass

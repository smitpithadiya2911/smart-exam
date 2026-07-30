from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile

@receiver(post_save, sender=StudentProfile)
def student_profile_saved_signal(sender, instance, created, **kwargs):
    pass

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TeacherProfile

@receiver(post_save, sender=TeacherProfile)
def teacher_profile_saved_signal(sender, instance, created, **kwargs):
    pass

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Semester

@receiver(post_save, sender=Semester)
def semester_saved_signal(sender, instance, created, **kwargs):
    pass

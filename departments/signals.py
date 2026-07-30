from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Department

@receiver(post_save, sender=Department)
def department_saved_signal(sender, instance, created, **kwargs):
    pass

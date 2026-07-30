from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Certificate

@receiver(post_save, sender=Certificate)
def certificate_saved_signal(sender, instance, created, **kwargs):
    pass

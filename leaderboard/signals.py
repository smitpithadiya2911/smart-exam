from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserBadge

@receiver(post_save, sender=UserBadge)
def user_badge_saved_signal(sender, instance, created, **kwargs):
    pass

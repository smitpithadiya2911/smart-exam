from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AIStudyRecommendation

@receiver(post_save, sender=AIStudyRecommendation)
def recommendation_saved_signal(sender, instance, created, **kwargs):
    pass

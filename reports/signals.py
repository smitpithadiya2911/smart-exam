from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SystemReportLog

@receiver(post_save, sender=SystemReportLog)
def report_saved_signal(sender, instance, created, **kwargs):
    pass

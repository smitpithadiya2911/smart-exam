from django.db import models
from django.conf import settings

class AchievementBadge(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default='trophy-fill')
    color_hex = models.CharField(max_length=20, default='#f59e0b')

    def __str__(self):
        return f"{self.title} ({self.code})"

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(AchievementBadge, on_delete=models.CASCADE, related_name='awarded_users')
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-awarded_at']

    def __str__(self):
        return f"{self.user.get_full_name()} -> {self.badge.title}"

from django.contrib import admin
from .models import AchievementBadge, UserBadge

@admin.register(AchievementBadge)
class AchievementBadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'icon_name', 'color_hex')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')

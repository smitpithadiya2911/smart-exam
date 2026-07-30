from rest_framework import serializers
from .models import AchievementBadge, UserBadge

class AchievementBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementBadge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = AchievementBadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = '__all__'

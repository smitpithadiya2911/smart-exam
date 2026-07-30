from rest_framework import serializers
from .models import AIStudyRecommendation

class AIStudyRecommendationSerializer(serializers.ModelSerializer):
    student_email = serializers.ReadOnlyField(source='student.email')

    class Meta:
        model = AIStudyRecommendation
        fields = '__all__'

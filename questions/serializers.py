from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_code = serializers.ReadOnlyField(source='subject.code')

    class Meta:
        model = Question
        fields = '__all__'

from rest_framework import serializers
from .models import AnswerAttempt
from exams.serializers import ExamAttemptSerializer
from questions.serializers import QuestionSerializer

class AnswerAttemptSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = AnswerAttempt
        fields = '__all__'

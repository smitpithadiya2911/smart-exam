from rest_framework import serializers
from .models import Exam, ExamAttempt, AttemptViolation
from questions.serializers import QuestionSerializer

class ExamSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_code = serializers.ReadOnlyField(source='subject.code')

    class Meta:
        model = Exam
        fields = '__all__'

class AttemptViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptViolation
        fields = '__all__'

class ExamAttemptSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    exam_title = serializers.ReadOnlyField(source='exam.title')
    violations = AttemptViolationSerializer(many=True, read_only=True)

    class Meta:
        model = ExamAttempt
        fields = '__all__'

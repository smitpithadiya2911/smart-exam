from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    exam_title = serializers.ReadOnlyField(source='exam.title')

    class Meta:
        model = Certificate
        fields = '__all__'

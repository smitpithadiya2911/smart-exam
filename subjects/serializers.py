from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    semester_name = serializers.ReadOnlyField(source='semester.name')
    teacher_name = serializers.ReadOnlyField(source='assigned_teacher.get_full_name')

    class Meta:
        model = Subject
        fields = '__all__'

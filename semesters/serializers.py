from rest_framework import serializers
from .models import Semester

class SemesterSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = Semester
        fields = '__all__'

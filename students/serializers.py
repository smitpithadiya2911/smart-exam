from rest_framework import serializers
from .models import StudentProfile
from accounts.serializers import UserSerializer

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.ReadOnlyField(source='department.name')
    course_name = serializers.ReadOnlyField(source='course.name')
    semester_name = serializers.ReadOnlyField(source='semester.name')

    class Meta:
        model = StudentProfile
        fields = '__all__'

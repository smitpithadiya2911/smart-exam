from rest_framework import serializers
from .models import TeacherProfile
from accounts.serializers import UserSerializer

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = TeacherProfile
        fields = '__all__'

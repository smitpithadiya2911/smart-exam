from rest_framework import serializers
from .models import SystemReportLog

class SystemReportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemReportLog
        fields = '__all__'

from django.contrib import admin
from .models import SystemReportLog

@admin.register(SystemReportLog)
class SystemReportLogAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'generated_by', 'format', 'timestamp')

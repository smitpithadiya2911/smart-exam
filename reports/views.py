from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.permissions import role_required
from .models import SystemReportLog
from .services import ReportGeneratorService

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def reports_dashboard_view(request):
    logs = SystemReportLog.objects.all()[:20]
    return render(request, 'reports/reports_dashboard.html', {'logs': logs})

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def export_students_excel_view(request):
    SystemReportLog.objects.create(report_name="Students Performance Report", generated_by=request.user.email, format="Excel")
    return ReportGeneratorService.export_students_excel()

@login_required
@role_required(['SUPER_ADMIN', 'TEACHER'])
def export_exams_pdf_view(request):
    SystemReportLog.objects.create(report_name="System Exams Summary Report", generated_by=request.user.email, format="PDF")
    return ReportGeneratorService.export_exams_summary_pdf()

from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard_view, name='reports_dashboard'),
    path('export/students-excel/', views.export_students_excel_view, name='export_students_excel'),
    path('export/exams-pdf/', views.export_exams_pdf_view, name='export_exams_pdf'),
]

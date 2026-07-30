from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:attempt_id>/', views.result_detail_view, name='result_detail'),
    path('<uuid:attempt_id>/pdf/', views.download_result_pdf_view, name='download_result_pdf'),
    path('<uuid:attempt_id>/grade/', views.teacher_manual_grading_view, name='manual_grading'),
    path('save-manual-grade/', views.save_manual_grade_ajax, name='save_manual_grade'),
]

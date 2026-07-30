from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('ai-recommendations/', views.ai_recommendations_view, name='ai_recommendations'),
    path('download-timetable/', views.download_timetable_view, name='download_timetable'),
    path('chart-data/', views.chart_data_api, name='chart_data_api'),
    path('live-search/', views.live_search_view, name='live_search_api'),
]

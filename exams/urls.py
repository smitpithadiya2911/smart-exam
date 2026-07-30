from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list_view, name='exam_list'),
    path('create/', views.exam_create_view, name='exam_create'),
    path('<uuid:pk>/edit/', views.exam_edit_view, name='exam_edit'),
    path('<uuid:pk>/delete/', views.exam_delete_view, name='exam_delete'),
    path('upcoming/', views.student_upcoming_exams_view, name='student_upcoming_exams'),
    path('<uuid:pk>/instructions/', views.exam_instructions_view, name='exam_instructions'),
    path('take/<uuid:attempt_id>/', views.start_exam_view, name='start_exam'),
    path('autosave/', views.autosave_answer_ajax, name='autosave_answer'),
    path('log-violation/', views.log_violation_ajax, name='log_violation'),
    path('submit/<uuid:attempt_id>/', views.submit_exam_view, name='submit_exam'),
]

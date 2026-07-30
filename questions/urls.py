from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list_view, name='question_list'),
    path('add/', views.question_create_view, name='question_create'),
    path('<int:pk>/edit/', views.question_edit_view, name='question_edit'),
    path('<int:pk>/delete/', views.question_delete_view, name='question_delete'),
    path('export/', views.question_export_excel_view, name='question_export'),
    path('import/', views.question_import_excel_view, name='question_import'),
]

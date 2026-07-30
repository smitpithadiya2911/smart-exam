from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list_view, name='subject_list'),
    path('<int:pk>/edit/', views.subject_edit_view, name='subject_edit'),
    path('<int:pk>/delete/', views.subject_delete_view, name='subject_delete'),
]

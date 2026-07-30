from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list_view, name='teacher_list'),
    path('<int:pk>/edit/', views.teacher_edit_view, name='teacher_edit'),
    path('<int:pk>/delete/', views.teacher_delete_view, name='teacher_delete'),
]

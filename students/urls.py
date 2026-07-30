from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list_view, name='student_list'),
    path('<int:pk>/edit/', views.student_edit_view, name='student_edit'),
    path('<int:pk>/delete/', views.student_delete_view, name='student_delete'),
]

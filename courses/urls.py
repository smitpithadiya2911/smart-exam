from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('<int:pk>/edit/', views.course_edit_view, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete_view, name='course_delete'),
]

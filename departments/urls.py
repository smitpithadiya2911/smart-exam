from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list_view, name='department_list'),
    path('<int:pk>/edit/', views.department_edit_view, name='department_edit'),
    path('<int:pk>/delete/', views.department_delete_view, name='department_delete'),
]

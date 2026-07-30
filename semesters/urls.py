from django.urls import path
from . import views

urlpatterns = [
    path('', views.semester_list_view, name='semester_list'),
    path('<int:pk>/edit/', views.semester_edit_view, name='semester_edit'),
    path('<int:pk>/delete/', views.semester_delete_view, name='semester_delete'),
]

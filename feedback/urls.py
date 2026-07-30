from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list_view, name='feedback_list'),
    path('<int:pk>/toggle-approval/', views.toggle_feedback_approval_view, name='toggle_feedback_approval'),
]

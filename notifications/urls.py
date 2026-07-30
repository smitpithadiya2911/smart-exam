from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list_view, name='notification_list'),
    path('<int:pk>/read/', views.mark_notification_read_ajax, name='mark_notification_read'),
    path('read-all/', views.mark_all_read_ajax, name='mark_all_read'),
    path('broadcast/', views.broadcast_announcement_view, name='broadcast_announcement'),
]

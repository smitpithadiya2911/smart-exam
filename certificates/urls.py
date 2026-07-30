from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list_view, name='certificate_list'),
    path('<str:uuid_str>/', views.certificate_detail_view, name='certificate_detail'),
    path('verify/<str:uuid_str>/', views.public_verify_certificate_view, name='verify_certificate_public'),
]

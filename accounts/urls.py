from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_student_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('ajax/send-email-otp/', views.ajax_send_email_otp_view, name='ajax_send_email_otp'),
    path('ajax/send-phone-otp/', views.ajax_send_phone_otp_view, name='ajax_send_phone_otp'),
        path('dashboard/', views.dashboard_redirect_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('toggle-dark-mode/', views.toggle_dark_mode_view, name='toggle_dark_mode'),
    path('login-history/', views.login_history_view, name='login_history'),
    path('toggle-user-active/<uuid:user_id>/', views.toggle_user_active_view, name='toggle_user_active'),
]

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_student_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/forgot_password.html',
        success_url=reverse_lazy('login')
    ), name='forgot_password'),
        path('dashboard/', views.dashboard_redirect_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('toggle-dark-mode/', views.toggle_dark_mode_view, name='toggle_dark_mode'),
    path('login-history/', views.login_history_view, name='login_history'),
    path('toggle-user-active/<uuid:user_id>/', views.toggle_user_active_view, name='toggle_user_active'),
]

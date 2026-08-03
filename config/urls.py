"""
URL Configuration for Smart Online Examination & Learning Analytics System.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin.site.site_header = "Smart Online Examination Admin Panel"
admin.site.site_title = "Smart Exam Admin"
admin.site.index_title = "Academic Operations & Database Management Hub"

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('login/admin/', RedirectView.as_view(url='/admin/', permanent=True)),
    path('login/admin', RedirectView.as_view(url='/admin/', permanent=True)),

    path('accounts/', include('allauth.urls')),


    # Web App URL Routing
    path('', include('accounts.urls')),
    path('departments/', include('departments.urls')),
    path('courses/', include('courses.urls')),
    path('semesters/', include('semesters.urls')),
    path('subjects/', include('subjects.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('questions/', include('questions.urls')),
    path('exams/', include('exams.urls')),
    path('results/', include('results.urls')),
    path('analytics/', include('analytics.urls')),
    path('notifications/', include('notifications.urls')),
    path('certificates/', include('certificates.urls')),
    path('feedback/', include('feedback.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('reports/', include('reports.urls')),

    # REST API & Documentation
    path('api/v1/', include('api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

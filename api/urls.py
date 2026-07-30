from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'exams', views.ExamViewSet, basename='exam')
router.register(r'attempts', views.ExamAttemptViewSet, basename='attempt')
router.register(r'certificates', views.CertificateViewSet, basename='certificate')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]

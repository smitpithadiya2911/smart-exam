from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from departments.models import Department
from courses.models import Course
from semesters.models import Semester
from subjects.models import Subject
from exams.models import Exam, ExamAttempt
from .models import Certificate
from .services import CertificateService

class CertificateServiceTest(TestCase):
    def test_certificate_generation(self):
        user = User.objects.create_user(email='prof@exam.com', password='pass', role=User.Role.TEACHER)
        student = User.objects.create_user(email='student@exam.com', password='pass', role=User.Role.STUDENT)
        dept = Department.objects.create(name='CS', code='CS')
        course = Course.objects.create(name='BCA', code='BCA', department=dept)
        sem = Semester.objects.create(course=course, number=1, name='Sem 1', start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=180))
        subject = Subject.objects.create(semester=sem, name='C Prog', code='BCA101')
        exam = Exam.objects.create(title='Midterm', subject=subject, created_by=user, start_time=timezone.now(), end_time=timezone.now()+timedelta(hours=1), duration_minutes=60, total_marks=100, passing_marks=40)
        attempt = ExamAttempt.objects.create(exam=exam, student=student, status=ExamAttempt.Status.COMPLETED, total_score=85, percentage=85.0, is_passed=True)

        cert = CertificateService.generate_certificate(attempt)
        self.assertIsNotNone(cert.certificate_uuid)
        self.assertEqual(cert.student, student)

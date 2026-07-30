from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from departments.models import Department
from courses.models import Course
from semesters.models import Semester
from subjects.models import Subject
from exams.models import Exam

class ExamModelTest(TestCase):
    def test_exam_creation(self):
        user = User.objects.create_user(email='prof@exam.com', password='pass', role=User.Role.TEACHER)
        dept = Department.objects.create(name='CS', code='CS')
        course = Course.objects.create(name='BCA', code='BCA', department=dept)
        sem = Semester.objects.create(course=course, number=1, name='Sem 1', start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=180))
        subject = Subject.objects.create(semester=sem, name='C Prog', code='BCA101')

        start = timezone.now()
        end = start + timedelta(hours=2)
        exam = Exam.objects.create(
            title='Midterm', subject=subject, created_by=user,
            start_time=start, end_time=end, duration_minutes=60,
            total_marks=100, passing_marks=40, is_published=True
        )
        self.assertEqual(exam.title, 'Midterm')
        self.assertTrue(exam.is_active)

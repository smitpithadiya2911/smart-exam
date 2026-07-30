from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from departments.models import Department
from courses.models import Course
from semesters.models import Semester
from .models import Subject

class SubjectModelTest(TestCase):
    def test_subject_creation(self):
        dept = Department.objects.create(name='CS', code='CS')
        course = Course.objects.create(name='BCA', code='BCA', department=dept)
        sem = Semester.objects.create(course=course, number=1, name='Sem 1', start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=180))
        subject = Subject.objects.create(semester=sem, name='C Programming', code='BCA101', credits=4)
        self.assertEqual(subject.code, 'BCA101')

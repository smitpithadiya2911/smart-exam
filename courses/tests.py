from django.test import TestCase
from departments.models import Department
from .models import Course

class CourseModelTest(TestCase):
    def test_course_creation(self):
        dept = Department.objects.create(name='IT', code='IT')
        course = Course.objects.create(name='B.Sc IT', code='BSCIT', department=dept, duration_years=3)
        self.assertEqual(course.code, 'BSCIT')
        self.assertEqual(course.department, dept)

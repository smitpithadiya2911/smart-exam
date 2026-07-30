from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from departments.models import Department
from courses.models import Course
from .models import Semester

class SemesterModelTest(TestCase):
    def test_semester_date_validation(self):
        dept = Department.objects.create(name='CS', code='CS')
        course = Course.objects.create(name='BCA', code='BCA', department=dept)
        start = timezone.now().date()
        end = start + timedelta(days=180)
        sem = Semester.objects.create(course=course, number=1, name='Sem 1', start_date=start, end_date=end)
        self.assertEqual(sem.number, 1)

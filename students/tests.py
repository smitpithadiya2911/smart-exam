from django.test import TestCase
from accounts.models import User
from .models import StudentProfile

class StudentProfileModelTest(TestCase):
    def test_student_profile(self):
        user = User.objects.create_user(email='teststudent@exam.com', password='pass', first_name='John', last_name='Doe')
        profile = StudentProfile.objects.create(user=user, roll_number='BCA2026-001')
        self.assertEqual(profile.roll_number, 'BCA2026-001')

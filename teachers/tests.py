from django.test import TestCase
from accounts.models import User
from .models import TeacherProfile

class TeacherProfileModelTest(TestCase):
    def test_teacher_profile(self):
        user = User.objects.create_user(email='prof@exam.com', password='pass', first_name='Alan', last_name='Turing', role=User.Role.TEACHER)
        profile = TeacherProfile.objects.create(user=user, employee_id='EMP101', designation='Professor')
        self.assertEqual(profile.employee_id, 'EMP101')

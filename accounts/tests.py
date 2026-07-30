from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='student@example.com',
            password='password123',
            first_name='Student',
            last_name='User'
        )
        self.assertEqual(user.email, 'student@example.com')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            first_name='Super',
            last_name='Admin'
        )
        self.assertEqual(admin.role, User.Role.SUPER_ADMIN)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class GoogleLoginTests(TestCase):
    def test_google_login_mock_new_user(self):
        # Sending mock credentials creates a new student user
        response = self.client.post('/google-login/', {
            'credential': 'mock_newstudent@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
        
        # Verify the user was created as a student
        user = User.objects.get(email='newstudent@example.com')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.first_name, 'Newstudent')
        
        # Verify student profile exists
        from students.models import StudentProfile
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())

    def test_google_login_mock_existing_user(self):
        # Create an existing user first
        existing_user = User.objects.create_user(
            email='smitpithadiya@gmail.com',
            password='Smit#2911',
            first_name='Smit',
            last_name='Pithadiya',
            role=User.Role.SUPER_ADMIN
        )
        existing_user.is_superuser = True
        existing_user.is_staff = True
        existing_user.save()

        # Log in with Google mock flow
        response = self.client.post('/google-login/', {
            'credential': 'mock_smitpithadiya@gmail.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
        
        # Verify that we are logged in as the superuser
        user = User.objects.get(email='smitpithadiya@gmail.com')
        self.assertEqual(user.role, User.Role.SUPER_ADMIN)
        self.assertTrue(user.is_superuser)

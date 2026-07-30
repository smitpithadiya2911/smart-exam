from django.test import TestCase
from accounts.models import User
from .models import Feedback

class FeedbackTest(TestCase):
    def test_feedback_creation(self):
        user = User.objects.create_user(email='test@exam.com', password='pass')
        fb = Feedback.objects.create(user=user, rating=5, comments='Great exam system!')
        self.assertEqual(fb.rating, 5)
        self.assertTrue(fb.is_approved)

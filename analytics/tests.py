from django.test import TestCase
from accounts.models import User
from .services import AIRecommendationService

class AIRecommendationTest(TestCase):
    def test_empty_recommendations(self):
        student = User.objects.create_user(email='test@exam.com', password='pass', role=User.Role.STUDENT)
        res = AIRecommendationService.generate_recommendations_for_student(student)
        self.assertIn('weak_topic_recs', res)
        self.assertEqual(res['trend_label'], 'Stable')

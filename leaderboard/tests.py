from django.test import TestCase
from accounts.models import User
from .services import LeaderboardService

class LeaderboardTest(TestCase):
    def test_rankings(self):
        user = User.objects.create_user(email='test@exam.com', password='pass', role=User.Role.STUDENT)
        LeaderboardService.evaluate_badges_for_student(user)
        rankings = LeaderboardService.get_leaderboard_rankings()
        self.assertIsNotNone(rankings)

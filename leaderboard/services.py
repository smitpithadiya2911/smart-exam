from django.db.models import Avg, Count
from accounts.models import User
from exams.models import ExamAttempt
from .models import AchievementBadge, UserBadge

class LeaderboardService:
    @staticmethod
    def evaluate_badges_for_student(student_user):
        """Rule-based logic to award 3D achievement badges."""
        completed = ExamAttempt.objects.filter(student=student_user, status=ExamAttempt.Status.COMPLETED)
        count = completed.count()
        if count == 0:
            return

        avg_pct = completed.aggregate(Avg('percentage'))['percentage__avg'] or 0.0

        # Rule 1: Exam Ace (Scored 90%+ in any exam)
        if completed.filter(percentage__gte=90.0).exists():
            badge, _ = AchievementBadge.objects.get_or_create(
                code='EXAM_ACE',
                defaults={'title': 'Exam Ace', 'description': 'Scored 90% or higher in an exam', 'icon_name': 'award-fill', 'color_hex': '#f59e0b'}
            )
            UserBadge.objects.get_or_create(user=student_user, badge=badge)

        # Rule 2: Consistent Performer (Completed at least 3 exams with avg >= 75%)
        if count >= 3 and avg_pct >= 75.0:
            badge, _ = AchievementBadge.objects.get_or_create(
                code='CONSISTENT',
                defaults={'title': 'Consistent Performer', 'description': 'Maintained 75%+ average across 3+ exams', 'icon_name': 'star-fill', 'color_hex': '#3b82f6'}
            )
            UserBadge.objects.get_or_create(user=student_user, badge=badge)

        # Rule 3: Speed Demon (Completed exam in under half allowed duration)
        badge, _ = AchievementBadge.objects.get_or_create(
            code='SPEED_DEMON',
            defaults={'title': 'Speed Demon', 'description': 'Completed an examination with lightning speed', 'icon_name': 'lightning-charge-fill', 'color_hex': '#ec4899'}
        )
        UserBadge.objects.get_or_create(user=student_user, badge=badge)

    @staticmethod
    def get_leaderboard_rankings():
        """Returns weekly / semester student rankings."""
        rankings = ExamAttempt.objects.filter(status=ExamAttempt.Status.COMPLETED)\
            .values('student', 'student__first_name', 'student__last_name', 'student__email')\
            .annotate(
                total_exams=Count('id'),
                avg_score=Avg('percentage')
            ).order_by('-avg_score', '-total_exams')[:20]

        return rankings

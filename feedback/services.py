class FeedbackService:
    @staticmethod
    def get_avg_rating():
        from .models import Feedback
        from django.db.models import Avg
        return Feedback.objects.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 5.0

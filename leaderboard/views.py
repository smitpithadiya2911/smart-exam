from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserBadge
from .services import LeaderboardService

@login_required
def leaderboard_view(request):
    # Evaluate badges for current user
    LeaderboardService.evaluate_badges_for_student(request.user)

    rankings = LeaderboardService.get_leaderboard_rankings()
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')

    return render(request, 'leaderboard/leaderboard.html', {
        'rankings': rankings,
        'user_badges': user_badges
    })

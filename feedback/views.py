from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.permissions import role_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def feedback_list_view(request):
    if request.user.role == 'SUPER_ADMIN':
        feedbacks = Feedback.objects.all().select_related('user', 'exam')
    else:
        feedbacks = Feedback.objects.filter(is_approved=True).select_related('user', 'exam')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.save()
            messages.success(request, "Thank you! Your feedback has been submitted successfully.")
            return redirect('feedback_list')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_list.html', {
        'feedbacks': feedbacks,
        'form': form
    })

@login_required
@role_required(['SUPER_ADMIN'])
def toggle_feedback_approval_view(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    fb.is_approved = not fb.is_approved
    fb.save(update_fields=['is_approved'])
    messages.success(request, f"Feedback status updated to {'Approved' if fb.is_approved else 'Hidden'}.")
    return redirect('feedback_list')

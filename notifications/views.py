from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from accounts.permissions import role_required
from .models import Notification
from .forms import AnnouncementForm
from .services import NotificationService

@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
@require_POST
def mark_notification_read_ajax(request, pk):
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def mark_all_read_ajax(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
@role_required(['SUPER_ADMIN'])
def broadcast_announcement_view(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            count = NotificationService.broadcast_announcement(title, message, request.user)
            messages.success(request, f"Broadcast announcement sent to {count} users!")
            return redirect('notification_list')
    else:
        form = AnnouncementForm()
    return render(request, 'notifications/broadcast.html', {'form': form})

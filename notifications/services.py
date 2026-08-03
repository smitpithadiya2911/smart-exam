from accounts.models import User
from .models import Notification

class NotificationService:
    @staticmethod
    def send_notification(recipient, title, message, link=None, n_type=Notification.Type.ANNOUNCEMENT):
        return Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            link=link,
            notification_type=n_type
        )

    @staticmethod
    def broadcast_announcement(title, message, sender_user):
        users = User.objects.filter(is_active=True)
        notifications = [
            Notification(
                recipient=u,
                title=title,
                message=message,
                notification_type=Notification.Type.ANNOUNCEMENT
            )
            for u in users
        ]
        Notification.objects.bulk_create(notifications)
        return len(notifications)

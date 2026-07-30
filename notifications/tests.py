from django.test import TestCase
from accounts.models import User
from .models import Notification
from .services import NotificationService

class NotificationTest(TestCase):
    def test_send_and_read_notification(self):
        user = User.objects.create_user(email='test@exam.com', password='pass')
        notif = NotificationService.send_notification(user, 'Test Alert', 'Body text')
        self.assertEqual(notif.is_read, False)
        notif.is_read = True
        notif.save()
        self.assertTrue(Notification.objects.get(id=notif.id).is_read)

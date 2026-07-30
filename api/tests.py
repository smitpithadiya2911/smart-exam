from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User

class ApiEndpointTest(TestCase):
    def test_users_api_unauthorized(self):
        client = APIClient()
        res = client.get('/api/v1/users/')
        self.assertEqual(res.status_code, 403)

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from api.v1.common.models import User

class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            phone_number='+1234567890'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user_profile')

    def test_get_user_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['phone_number'], '+1234567890')

    def test_update_user_profile(self):
        data = {
            'phone_number': '+0987654321'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['phone_number'], '+0987654321')
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.v1.common.models import User

class EmailVerificationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register_company')
        self.verify_url = reverse('verify_email')
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "fname": "Test",
            "lname": "User",
            "phone_number": "+1234567890",
            "business_name": "Test Business",
            "profile_picture": None,
            "is_company": True
        }

    def test_register_user_and_send_verification_email(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user.email_verification_code)

    def test_verify_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email=self.user_data['email'])
        verification_data = {
            "email": self.user_data['email'],
            "code": user.email_verification_code
        }
        response = self.client.post(self.verify_url, verification_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertIsNone(user.email_verification_code)
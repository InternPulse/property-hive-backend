from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')  # Login endpoint
        self.protected_url = reverse('protected')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword123',
            'user_type': 'individual',
        }

    def test_user_registration(self):
        """Test that a user can register successfully."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)

    def test_user_registration_missing_email(self):
        """Test registration fails with missing email."""
        data = self.user_data.copy()
        data['email'] = ''
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_protected_view_access(self):
        """Test that a logged-in user can access a protected view."""
        # Register and log in the user
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Now access the protected view
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have access to this protected view!')

    def test_protected_view_access_without_login(self):
        """Test that a user cannot access a protected view without logging in."""
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login(self):
        """Test that a user can log in and receive tokens."""
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')

        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """Test that login fails with invalid credentials."""
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')

        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

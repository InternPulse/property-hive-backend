from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.v1.common.models import User
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core import signing

# Create your tests here.


class ForgotPasswordViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('forgot-password')
        self.user_email = 'testuser@example.com'
        self.user = User.objects.create_user(
            fname='test', lname='user', email=self.user_email, password='testpassword123'
        )
    
    def test_password_reset_request_success(self):
        """Test if the password reset link is successfully sent when a valid email is provided."""
        response = self.client.post(self.url, {'email': self.user_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset email sent.')

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user_email, mail.outbox[0].to)

    
    def test_password_reset_request_email_not_found(self):
        """Test if the API returns 404 when the email is not found."""
        response = self.client.post(self.url, {'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'email not found.')

    def test_password_reset_request_invalid_email(self):
        """Test if the API returns 400 for an invalid email format."""
        response = self.client.post(self.url, {'email': 'invalid-email'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)



class ResetPasswordTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(fname='test', lname='user', email='test@example.com', password='old_password')

        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

        self.signed_data = signing.dumps({"uid" : self.uid, 'token' : self.token})
        self.url = reverse('reset-password')


    def test_reset_password_valid(self):
        data = {
            "token": self.signed_data,
            "newPassword": "new_strong_password123!"
        }
        
        # Send a POST request with valid token and new password
        response = self.client.post(self.url, data=data)
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        
        # Check if the password was actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_strong_password123!'))


    def test_reset_password_invalid_token(self):
        data = {
            "token": "invalid_token",
            "newPassword": "new_password123!"
        }
        
        # Send a POST request with an invalid token
        response = self.client.post(self.url, data=data)
        
        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)


    def test_reset_password_missing_password(self):
        data = {
            "token": self.token
            # No 'new_password' in the payload
        }
        
        # Send a POST request without the new password
        response = self.client.post(self.url, data=data)
        
        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("newPassword", response.data)

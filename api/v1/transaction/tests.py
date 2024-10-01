# api/v1/transaction/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Transactions
from .serializers import TransactionSerializer

User = get_user_model()

class TransactionDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',  # Assuming your user model uses email
            password='testpass'
        )
        self.transaction = Transactions.objects.create(
            userid=self.user,
            payment_method='Credit Card',
            total_amount=100.00
        )

    def test_get_transaction_detail_success(self):
        self.client.login(email='testuser@example.com', password='testpass')
        response = self.client.get(
            reverse('transaction-detail', kwargs={'transaction_id': self.transaction.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction_not_found(self):
        self.client.login(email='testuser@example.com', password='testpass')
        response = self.client.get(
            reverse('transaction-detail', kwargs={'transaction_id': 999}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_get_transaction_detail_unauthenticated(self):
         response = self.client.get(
            reverse('transaction-detail', kwargs={'transaction_id': self.transaction.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Adjusted to 403








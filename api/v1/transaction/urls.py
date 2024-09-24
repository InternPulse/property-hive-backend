# api/v1/transaction/urls.py

from django.urls import path
from .views import TransactionListView, TransactionDetailView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:transaction_id>/', TransactionDetailView.as_view(), name='transaction-detail'),
]

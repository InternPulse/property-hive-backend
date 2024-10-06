# api/v1/transaction/urls.py

from django.urls import path
from .views import TransactionListView, TransactionDetailView,PropertyInvoiceView,EarningDetailsView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:transaction_id>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('invoice/', PropertyInvoiceView.as_view(), name='invoice'),
    path('invoice/<int:invoice_id>/', PropertyInvoiceView.as_view(), name='invoice'),
    path('earnings/', EarningDetailsView.as_view(), name='earning-details'),
]

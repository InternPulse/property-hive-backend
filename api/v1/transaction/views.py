# api/v1/transaction/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from api.v1.common.models import Transactions,Invoice
from .serializers import TransactionSerializer,PropertyInvoiceSerializer, EarningDetailsSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transactions.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, transaction_id):
        try:
            return Transactions.objects.get(id=transaction_id)
        except Transactions.DoesNotExist:
            return None

    def get(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PropertyInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_id=None):
        # Use get_object_or_404 to handle the case when invoice is not found
        invoice = get_object_or_404(Invoice, id=invoice_id)

        # Serialize the invoice
        serializer = PropertyInvoiceSerializer(invoice)

        # Return a proper Response
        return Response({
            "message": "Invoice retrieved successfully",
            "status_code": 200,
            "data": serializer.data
        }, status=200)
    

class EarningDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        #total
        total_earnings = Transactions.objects.filter(userid=user, status=Transactions.Status.CREDIT_SUCCESS).aggregate(total=Sum('total_amount'))['total'] or 0
        #available
        available_earnings = total_earnings - withdrawn_earnings
        #pending
        pending_earnings = Transactions.objects.filter(userid=user, status=Transactions.Status.PENDING, payment_method='debit').aggregate(total=Sum('total_amount'))['total'] or 0
        #withdrawn
        withdrawn_earnings = Transactions.objects.filter(userid=user, status=Transactions.Status.DEBIT_SUCCESS).aggregate(total=Sum('total_amount'))['total'] or 0


        earnings_data = {
            'total_earnings': total_earnings,
            'available_earnings': available_earnings,
            'pending_earnings': pending_earnings,
            'withdrawn_earnings': withdrawn_earnings,
        }

        serializer = EarningDetailsSerializer(earnings_data)

        return Response(serializer.data, status=status.HTTP_200_OK)



class EarningDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        #total
        total_earnings = Transactions.objects.filter(userid=user, status=Transactions.Status.CREDIT_SUCCESS).aggregate(total=Sum('total_amount'))['total'] or 0
        #available
        available_earnings = total_earnings - withdrawn_earnings
        #pending
        pending_earnings = Transactions.objects.filter(userid=user, status=Transactions.Status.PENDING, payment_method='debit').aggregate(total=Sum('total_amount'))['total'] or 0
        #withdrawn
        withdrawn_earnings = Transactions.objects.filter(userid=user, status=Transactions.Status.DEBIT_SUCCESS).aggregate(total=Sum('total_amount'))['total'] or 0


        earnings_data = {
            'total_earnings': total_earnings,
            'available_earnings': available_earnings,
            'pending_earnings': pending_earnings,
            'withdrawn_earnings': withdrawn_earnings,
        }

        serializer = EarningDetailsSerializer(earnings_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework import serializers
from api.v1.common.models import Transactions,Invoice

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'  # Adjust fields as necessary

class  PropertyInvoiceSerializer(serializers.ModelSerializer):
    transactionid = serializers.PrimaryKeyRelatedField(queryset=Transactions.objects.all())
    payment_status = serializers.CharField()
    payment_method = serializers.CharField()
    note = serializers.CharField()
    issue_date=serializers.DateTimeField()

    class Meta:
        model=Invoice
        fields = ['transactionid','payment_status','payment_method','note','issue_date']

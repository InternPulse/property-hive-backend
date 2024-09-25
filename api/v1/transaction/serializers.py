from rest_framework import serializers
from api.v1.common.models import Transactions

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'  # Adjust fields as necessary

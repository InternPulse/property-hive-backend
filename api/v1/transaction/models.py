from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Transactions(models.Model):
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transaction_transactions')

    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        SUCCESS = 'A', 'Success'
        FAILED = 'F', 'Failed'

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
    )
    payment_method = models.CharField(max_length=255, null=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']  # Orders by created_at in descending order
        indexes = [
            models.Index(fields=['userid']),  # Index on userid
        ]
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f'Transaction {self.id} - {self.total_amount} USD, Status: {self.get_status_display()}'

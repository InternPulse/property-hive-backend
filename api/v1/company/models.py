from django.db import models
from ..common.models import User


class RealEstateCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    custom_url = models.CharField(max_length=255, blank=True, null=True)

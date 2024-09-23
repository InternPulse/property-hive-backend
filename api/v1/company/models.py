from django.db import models
from ..common.models import User, Profile


class RealEstateCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    custom_url = models.CharField(max_length=255, blank=True, null=True)

class CompanyProfile(models.Model):
    phone_number = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_phone_number")
    company_address = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="company_address")
    company_logo = logo = models.ImageField(upload_to='media/', verbose_name='image')
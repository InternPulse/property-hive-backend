from ..common.models import User
from rest_framework import serializers
from .models import RealEstateCompany, CompanyProfile
from django.utils.text import slugify


class RealEstateSerialize(serializers.ModelSerializer):
    class Meta:
        model = RealEstateCompany
        fields = ["user", "custom_url"]




class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['phone_number', 'company_address', 'company_logo']


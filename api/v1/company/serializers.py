from ..common.models import User
from rest_framework import serializers
from .models import RealEstateCompany
from django.utils.text import slugify
from ..common.models import Profile


class RealEstateSerialize(serializers.ModelSerializer):
    class Meta:
        model = RealEstateCompany
        fields = ["user", "custom_url"]


class CompanyProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userid.phone_number')

    class Meta:
        model = Profile
        fields = ['phone_number', 'company_address', 'company_logo']


from ..common.models import User
from rest_framework import serializers
from .models import RealEstateCompany
from django.utils.text import slugify


class RealEstateSerialize(serializers.ModelSerializer):
    class Meta:
        model = RealEstateCompany
        fields = ["user", "custom_url"]

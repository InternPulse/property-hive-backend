from common.models import User
from rest_framework import serializers
from company.models import RealEstateCompany
from django.utils.text import slugify


class RealEstateSerialize(serializers.ModelSerializer):
    class Meta:
        model = RealEstateCompany
        fields = ["user", "custom_url"]

        def create(self, validated_data):
            user = validated_data.pop("user")
            base_slug = slugify(user.business_name)
            custom_url = f"{base_slug}.propertyhive.com"
            if RealEstateCompany.objects.filter(custom_url=custom_url).exists():
                raise serializers.ValidationError(
                    {"message": "This url is already taken"}
                )
            validated_data["custom_url"] = custom_url
            company = RealEstateCompany.objects.create(user=user, **validated_data)
            return company

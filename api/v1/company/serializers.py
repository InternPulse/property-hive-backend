from ..common.models import User
from rest_framework import serializers
from .models import RealEstateCompany
from django.utils.text import slugify
from api.v1.common.models import Profile,User,Property,PropertyImages,PropertyDocuments

class RealEstateSerialize(serializers.ModelSerializer):
    class Meta:
        model = RealEstateCompany
        fields = ["user", "custom_url"]


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ['id', 'img']  # Include 'id' for reference

class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocuments
        fields = ['id', 'document_type', 'img', 'file_path', 'created_at', 'updated_at']

class PropertySerializer(serializers.ModelSerializer):
    property_images = PropertyImageSerializer(many=True, read_only=True,)
    property_documents = PropertyDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'sellerid', 'name', 'state', 'city', 'address', 'description',
                  'squaremeters', 'property_type', 'price', 'is_sold', 'date_sold',
                  'created_at', 'updated_at', 'property_images', 'property_documents']

class CompanyProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userid.phone_number')  # Assuming phone_number is a field in User
    company_address = serializers.CharField()
    company_logo = serializers.ImageField()
    company_banner = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()
    instagram = serializers.CharField()
    linkedin = serializers.CharField()
    facebook = serializers.CharField()
    twitter = serializers.CharField()
    properties = PropertySerializer(many=True, read_only=True, source='userid.properties')  # Adjusted source

    class Meta:
        model = Profile  # Ensure this is the correct model
        fields = ['phone_number', 'company_address', 'company_logo', 'company_banner',
                  'title', 'description', 'instagram', 'linkedin', 'facebook',
                  'twitter', 'properties']

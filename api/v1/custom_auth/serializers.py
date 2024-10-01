
"""
User and UserProfile Serializers
================================

This module defines serializers used for managing user registration and profile updates. The `UserSerializer` is used to handle user creation and `UserProfileSerializer` is designed to update the user profile, including the phone number and identification documents.

Classes
-------
1. UserSerializer(serializers.ModelSerializer)
2. UserProfileSerializer(serializers.ModelSerializer)

Attributes
----------
1. UserSerializer:
   - email: str (User's email address)
   - fname: str (User's first name)
   - lname: str (User's last name)
   - password: str (User's password, write-only)
   - business_name: str (User's business name)
   - profile_picture: str (URL to the user's profile picture)
   - phone_number: str (User's phone number)
   - is_company: bool (True for company accounts)

2. UserProfileSerializer:
   - phone_number: str (Phone number to be updated)
   - identification_documents: file (Optional; user-uploaded document file)

Methods
-------
- create(self, validated_data): Handles the creation of a new user and ensures the password is set securely.
- update(self, instance, validated_data): Updates the user's phone number and stores identification documents if provided.

"""

from rest_framework import fields, serializers
from api.v1.common.models import User, KycDocuments
import re

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing `User` objects.

    Fields:
    -------
    - email: The email address of the user.
    - fname: The first name of the user.
    - lname: The last name of the user.
    - password: The user's password (write-only).
    - business_name: The business name, applicable for companies.
    - profile_picture: The URL or file path to the user's profile picture.
    - phone_number: The user's contact number.
    - is_company: Boolean flag indicating if the user is a company (automatically set to True).

    Extra:
    ------
    - The `password` field is write-only and handled securely during user creation.
    """

    class Meta:
        model = User
        fields = ['email', 'fname', 'lname', 'password', 'business_name', 'profile_picture', 'phone_number', 'is_company']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create and return a new `User` instance with the provided data.

        Parameters:
        -----------
        - validated_data: A dictionary containing user data like email, first name, last name, etc.

        Process:
        --------
        - The password is securely hashed and stored.
        - The `is_company` field is automatically set to `True` for the user.
        """
        validated_data['is_company'] = True
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the user's profile, such as phone number and identification documents.

    Fields:
    -------
    - phone_number: The user's phone number.
    - identification_documents: A file field for uploading identification documents (write-only and optional).

    Methods:
    --------
    - update(self, instance, validated_data): Updates the user's profile, specifically the phone number and identification documents.
    """

    identification_documents = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['phone_number', 'identification_documents']

    def update(self, instance, validated_data):
        """
        Update the user's profile information.

        Parameters:
        -----------
        - instance: The current `User` instance to be updated.
        - validated_data: A dictionary of updated profile information, such as phone number and documents.

        Process:
        --------
        - Updates the phone number if provided.
        - If identification documents are provided, they are stored in the `KycDocuments` model.
        """
        phone_number = validated_data.get('phone_number', None)
        identification_documents = validated_data.get('identification_documents', None)

        if phone_number:
            instance.phone_number = phone_number

        if identification_documents:
            KycDocuments.objects.create(userid=instance, document_file=identification_documents)

        instance.save()
        return instance



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
    newPassword = serializers.CharField(min_length=7, write_only=True, required=True)

    def validate_newPassword(self, value):
         if not re.search(r'[a-z]', value):
           raise serializers.ValidationError("Password must contain at least one lowercase letter.")
         if not re.search(r'[0-9]', value):
           raise serializers.ValidationError("Password must contain at least one digit.")

         return value



class CustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    fname = serializers.CharField(max_length=150, required=True)
    lname = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_password(self, value):
         if not re.search(r'[a-z]', value):
           raise serializers.ValidationError("Password must contain at least one lowercase letter.")
         if not re.search(r'[0-9]', value):
           raise serializers.ValidationError("Password must contain at least one digit.")

         return value

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=5)
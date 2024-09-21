"""
Models Documentation
====================

This module defines the database models used in the application. These include user management, property listings, transactions, and related features such as invoices and ratings.

Models
------
1. CustomUserManagement
2. User
3. KycDocuments
4. Property
5. PropertyImages
6. PropertyDocuments
7. SoldProperties
8. UserProperties
9. Transactions
10. Invoice
11. Ratings
12. Profile

Details
-------
Each model is designed to handle specific parts of the application, such as users, properties, transactions, and user ratings.

"""

from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManagement(UserManager):
    """
    Custom manager for the `User` model to handle user creation and management, including normal users, superusers, and company users.

    Methods:
    --------
    - _create_user(self, email, password, **extra_fields): Base method for creating any type of user.
    - create_user(self, email=None, password=None, **extra_fields): Creates a normal user.
    - create_superuser(self, email=None, password=None, **extra_fields): Creates a superuser.
    - create_company_user(self, email=None, password=None, **extra_fields): Creates a company user.
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("A valid email address is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def create_company_user(self, email=None, password=None, **extra_fields):
        """
        Creates a user with company-specific settings.
        """
        extra_fields.setdefault('user_type', 'company')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom `User` model to handle user-related fields and authentication.

    Fields:
    -------
    - email: Email address of the user (unique).
    - fname: First name of the user.
    - lname: Last name of the user.
    - business_name: Business name (for companies), unique.
    - phone_number: Contact number (unique).
    - profile_picture: Profile picture uploaded by the user.
    - custom_url: A custom URL provided by the user.
    - is_company: Flag to identify if the user is a company.
    - is_active, is_staff, is_superuser: Boolean flags for permissions.
    - date_joined: Timestamp for when the user joined.
    - last_login: Last login timestamp.

    Meta:
    -----
    - verbose_name: 'User'
    - verbose_name_plural: 'Users'
    """
    email = models.EmailField(blank=True, default='', unique=True)
    fname = models.CharField(max_length=255, blank=True)
    lname = models.CharField(max_length=255, blank=True)
    business_name = models.CharField(max_length=255, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    custom_url = models.URLField(max_length=500, blank=True, null=True)
    is_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManagement()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


class KycDocuments(models.Model):
    """
    Model for storing KYC (Know Your Customer) documents uploaded by users.

    Fields:
    -------
    - userid: ForeignKey to the `User` model.
    - document_type: Type of the document (e.g., ID, passport).
    - document_file: FileField for uploading the document.
    - status: Status of the document (pending, approved, rejected).
    - uploaded_at: Timestamp for when the document was uploaded.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=225, null=True, blank=True)
    document_file = models.FileField(upload_to='media/kyc_documents/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Property(models.Model):
    """
    Model for properties listed by users.

    Fields:
    -------
    - sellerid: ForeignKey to the `User` model (seller).
    - location: Location of the property.
    - description: Description of the property.
    - squaremeters: Size of the property.
    - property_type: Type of property (e.g., house, land).
    - price: Price of the property.
    - created_at: Timestamp for when the property was listed.
    - updated_at: Timestamp for when the property details were last updated.
    """
    sellerid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    squaremeters = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    price = models.IntegerField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PropertyImages(models.Model):
    """
    Model for storing property images.

    Fields:
    -------
    - propertyid: ForeignKey to the `Property` model.
    - img: Image of the property.
    """
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    img = models.ImageField(upload_to='property_img/', blank=True, null=True)


class PropertyDocuments(models.Model):
    """
    Model for storing property-related documents.

    Fields:
    -------
    - propertyid: ForeignKey to the `Property` model.
    - document_type: Type of document.
    - file_path: FileField for uploading the document.
    """
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_documents')
    document_type = models.CharField(max_length=225, null=True, blank=True)
    file_path = models.FileField(upload_to='media/kyc_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Soldproperties(models.Model):
    """
    Model for storing sold properties.

    Fields:
    -------
    - userid: ForeignKey to the `User` model (seller).
    - propertyid: ForeignKey to the `Property` model.
    - date_sold: Timestamp for when the property was sold.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_soldproperties')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_soldproperties')
    date_sold = models.DateTimeField(auto_now_add=True)


class UserProperties(models.Model):
    """
    Model for storing properties purchased by users.

    Fields:
    -------
    - userid: ForeignKey to the `User` model (buyer).
    - propertyid: ForeignKey to the `Property` model.
    - date_purchased: Timestamp for when the property was purchased.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_properties')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_properties')
    date_purchased = models.DateTimeField(auto_now_add=True)


class Transactions(models.Model):
    """
    Model for storing transaction details.

    Fields:
    -------
    - userid: ForeignKey to the `User` model.
    - propertyid: ForeignKey to the `Property` model.
    - status: Status of the transaction (pending, success, failed).
    - payment_method: Method of payment used.
    - total_amount: Total amount for the transaction.
    - created_at: Timestamp for when the transaction was created.
    - updated_at: Timestamp for when the transaction was last updated.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_transactions')
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        SUCCESS = 'A', 'Success'
        FAILED = 'F', 'Failed'

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
    """
    Model for storing invoices.

    Fields:
    -------
    - userid: ForeignKey to the `User` model.
    - propertyid: ForeignKey to the `Property` model.
    - transactionid: ForeignKey to the `Transactions` model.
    - amount: Amount for the invoice.
    - invoice_file: File for the invoice (optional).
    - created_at: Timestamp for when the invoice was generated.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_invoice')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_invoice')
    transactionid = models.ForeignKey(Transactions, on_delete=models.CASCADE, related_name='transaction_invoice')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_file = models.FileField(upload_to='media/invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Ratings(models.Model):
    """
    Model for storing ratings provided by users.

    Fields:
    -------
    - userid: ForeignKey to the `User` model (who rated).
    - propertyid: ForeignKey to the `Property` model (rated property).
    - rating: Rating score provided by the user.
    - feedback: Feedback or comments provided by the user.
    - created_at: Timestamp for when the rating was given.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_ratings')
    rating = models.IntegerField(default=0)
    feedback = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    """
    Model for storing user profiles.

    Fields:
    -------
    - userid: ForeignKey to the `User` model.
    - dob: Date of birth.
    - gender: Gender of the user.
    - address: Address of the user.
    - occupation: Occupation of the user.
    - updated_at: Timestamp for when the profile was last updated.
    """
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, null=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=225, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
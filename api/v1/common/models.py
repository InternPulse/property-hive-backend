from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField

class CustomUserManagement(UserManager):
    def _create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError("you have not provided a valid email address")
        email= self.normalize_email(email)
        user= self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_user(self,email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self,email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,password,**extra_fields)

    def create_company_user(self, email=None, password=None, **extra_fields):
         # Set the user type for company users
        extra_fields.setdefault('user_type', 'company')  # Set as company user type
        extra_fields.setdefault('is_staff', False)  # Company users don’t need admin access
        extra_fields.setdefault('is_superuser', False)  # Not a superuser

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email= models.EmailField(blank=True, default='', unique=True)
    fname = models.CharField(max_length=255, blank=True)
    lname = models.CharField(max_length=255, blank=True)
    business_name = models.CharField(max_length=255, blank=True ,unique=True ,null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    custom_url = models.URLField(max_length=500, blank=True, null=True)
    is_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined= models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True,null=True)
    updated_at= models.DateTimeField(auto_now=True)
    email_verification_code= models.CharField(max_length=5, blank=True, null=True)
    email_verification_expiry = models.DateTimeField(blank=True, null=True)


    objects = CustomUserManagement()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def generate_verification_code(self):
        import random
        self.email_verification_code = str(random.randint(10000, 99999))
        self.email_verification_expiry = timezone.now() + timedelta(minutes=10)
        self.save()

class KycDocuments(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=225, null=True, blank=True)
    document_file = models.FileField(upload_to='media/kyc_documents/', null=True, blank=True)  # Document file
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the document was uploaded




class Property(models.Model):
    sellerid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    name=models.CharField(max_length=100)
    state=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    description = models.TextField()
    squaremeters=models.CharField(max_length=255)
    property_type=models.CharField(max_length=255)
    number_of_bathrooms=models.IntegerField(null=True,blank=True)
    number_of_bedrooms=models.IntegerField(null=True,blank=True)
    installment_duration=models.CharField(max_length=255)
    payment_frequency=models.CharField(max_length=255)
    down_payment = models.TextField()
    installment_payment_price = models.IntegerField()
    keywords = models.CharField(max_length=1000, blank=True)
    price =models.IntegerField(null=False, blank=True)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_sold = models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class PropertyImages(models.Model):
     propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
     img = models.ImageField(upload_to='propery_img/', blank=True, null=True)



class PropertyDocuments(models.Model):
        propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_documents')
        document_type = models.CharField(max_length=225, null=True, blank=True)
        img = models.ImageField(upload_to='propery_img/', blank=True, null=True)
        file_path = models.FileField(upload_to='media/kyc_documents/', null=True, blank=True)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)




class Soldproperties(models.Model):
    buyerid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_soldproperties')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_soldproperties')
    date_sold=models.DateTimeField(auto_now_add=True)
    def clean(self):
        # Validate that the associated property is sold
        if not self.propertyid.is_sold:
            raise ValidationError("The property must be marked as sold to create a sale record.")

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method to enforce validation
        super().save(*args, **kwargs)

class Userproperties(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_properties')
    propertyid =  models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_properties')
    date_purchased = models.DateTimeField(auto_now_add=True)

class Transactions(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    propertyid =  models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_transactions')
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        CREDIT_SUCCESS = 'C', 'Credit Success'
        DEBIT_SUCCESS = 'D', 'Debit Success'
        FAILED = 'F', 'Failed'
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
    )
    payment_method = models.CharField(max_length=255,null=False)
    total_amount = models.IntegerField(null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Invoice(models.Model):
    transactionid=models.ForeignKey(Transactions, on_delete=models.CASCADE, related_name='invoices')
    payment_status=models.CharField(max_length=225,null=False)
    payment_method=models.CharField(max_length=225,null=False)
    note=models.TextField(null=True, blank=True)
    issue_date=models.DateTimeField(auto_now_add=True)

class Rate(models.IntegerChoices):
    ONE_STAR = 1, '1 Star'
    TWO_STAR = 2, '2 Stars'
    THREE_STAR = 3, '3 Stars'
    FOUR_STAR = 4, '4 Stars'
    FIVE_STAR = 5, '5 Stars'
class Ratings(models.Model):
     userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
     propertyid =  models.ForeignKey(Property, on_delete=models.CASCADE, related_name='propertyid_rating')
     comment=models.TextField( null=True)
     rate = models.IntegerField(
        choices=Rate.choices,
        default=Rate.ONE_STAR,
     )
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)

class Profile(models.Model):
     userid = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
     company_logo=models.ImageField(upload_to='company_profiles/', blank=True, null=True)
     company_banner=models.ImageField(upload_to='company_profiles/', blank=True, null=True)
     company_address=models.CharField(max_length=255, blank=True, null=True)
     title=models.CharField(max_length=50, blank=True, null=True)
     description= models.TextField(max_length=500)
     instagram=models.CharField(max_length=225, blank=True, null=True)
     linkedin=models.CharField(max_length=225, blank=True, null=True)
     facebook=models.CharField(max_length=225, blank=True, null=True)
     twitter=models.CharField(max_length=225, blank=True, null=True)

class CompanyView(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    viewed_on = models.DateField(default=timezone.now)
    views = models.IntegerField(default=1)

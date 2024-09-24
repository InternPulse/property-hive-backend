from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

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
    email= models.EmailField(blank=True, default='', unique=True)
    fname = models.CharField(max_length=255, blank=True)
    lname = models.CharField(max_length=255, blank=True)
    business_name = models.CharField(max_length=255, blank=True ,unique=True)
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

    objects = CustomUserManagement()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class KycDocuments(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=225, null=True, blank=True)
    document_file = models.FileField(upload_to='media/kyc_documents/', null=True, blank=True)  # Document file
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the document was uploaded




class Property(models.Model):
    sellerid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    location= models.CharField(max_length=255, )
    description = models.CharField(max_length=255)
    squaremeters=models.CharField(max_length=255)
    property_type=models.CharField(max_length=255)
    price =models.IntegerField(null=False, blank=True)
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
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_soldproperties')
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_soldproperties')
    # buyerid = models.ForeignKey(userid, on_delete=models.CASCADE, related_name='soldproperties')
    date_sold=models.DateTimeField(auto_now_add=True)

class Userproperties(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_properties')
    propertyid =  models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_properties')
    date_purchased = models.DateTimeField(auto_now_add=True)

class Transactions(models.Model):
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='common_transactions')
    propertyid =  models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_transactions')
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        SUCCESS = 'A', 'Success'
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
     status = models.IntegerField(
        choices=Rate.choices,
        default=Rate.ONE_STAR,
     )
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)

class Profile(models.Model):
     userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
     propertyid =  models.ForeignKey(Property, on_delete=models.CASCADE, related_name='soldproperties')
     company_address=models.CharField(max_length=255, blank=True, null=True)
     description= models.TextField(max_length=500)



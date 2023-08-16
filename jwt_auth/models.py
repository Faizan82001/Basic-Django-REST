from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
genders = ['Male', 'Female']
GENDER_CHOICES = [(gender, gender) for gender in genders]


class UserManager(BaseUserManager):
    def create_user(self, name, email, password, **other_fields):
        if not email:
            raise ValueError('You must enter an email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, name, email, password, **other_fields):
        other_fields.set_default('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must have "is_staff=True"')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have "is_superuser=True"')
        return self.create_user(email, name, password, **other_fields)
        
class Customer(AbstractBaseUser):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, unique=True)
    email = models.EmailField(blank=False, max_length=100, unique=True)
    password = models.CharField(blank=False, max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    address = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        db_table = "Customer"

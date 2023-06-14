from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save,post_delete
from helper import unique_code_generator 
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.dispatch import receiver
from django.conf import settings  
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        # create and save a user with the given email, phone and password
        # extra_fields can be any other fields defined in your user model
        if not email:
            raise ValueError("User must have an email address")
        if not phone:
            raise ValueError("User must have a phone number")
        user = self.model( email=self.normalize_email(email),phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        # create and save a superuser with the given email, phone and password
        # extra_fields can be any other fields defined in your user model
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, phone, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{1,10}$', message="Phone number must be entered in the format: '966453047'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def __str__(self):
        return self.first_name
    
class Role(Group):
    description = models.TextField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

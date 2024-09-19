from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

from app.models import Person

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        # Add more role choices as needed
    ]
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    twofactor_code = models.CharField(max_length=6, blank=True, null=True)

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    sub_unit = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
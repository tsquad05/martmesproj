from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    full_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    last_password_reset_request = models.DateTimeField(null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name}"
    


class UserToken(models.Model):
    TOKEN_TYPES = (
        ('email_confirmation', 'Email Confirmation'),
        ('password_reset', 'Password Reset'),
        ('refresh_token', 'Refresh token'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=20, choices=TOKEN_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Token'
        verbose_name_plural = 'User Tokens'

    def __str__(self):
        return f'Token: {self.token} - Type: {self.token_type}'

    def save(self, *args, **kwargs):
        # Set expiration time to 30 minutes from the current time
        self.expires_at = self.created_at + timezone.timedelta(days=1)
        super().save(*args, **kwargs)


class Contact(models.Model):
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    contact = models.PositiveBigIntegerField(default="+234123456789", null=True)
    email = models.EmailField()
    message = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Messages from clients"
    def __str__(self):
        return self.email
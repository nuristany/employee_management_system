from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import random


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValidationError('Superuser must have is_staff=True.')
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)    
    expires_at = models.DateTimeField()

    def generate_token(self):
        token = str(random.randint(100000, 999999))
        self.token = token
        self.expires_at = timezone.now() + timedelta(minutes=30)
        self.save()
        return token

    def is_valid(self):
        return self.expires_at > timezone.now()

    def verify_token(self, provided_token):
        return self.token == provided_token and self.is_valid()

    @staticmethod
    def cleanup_expired_tokens():
        PasswordResetToken.objects.filter(expires_at__lt=timezone.now()).delete()

    def __str__(self):
        return f"Token for {self.user.email}: {self.token}"

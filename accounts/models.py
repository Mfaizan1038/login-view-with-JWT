from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.customuser import CustomUserManager


class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []     

    objects = CustomUserManager()

    def __str__(self):
        return self.email

from django.contrib.auth.models import AbstractUser, BaseUserManager
# AbstractUser is Django’s default Class that defines the User model template. It Includes: password, email, username, is_staff, is_superuser, etc. You extend this to customize user.

# BaseUserManager is the Default Object Manager Class for user Class Objects. We need to use it here as we are using email instead of username for authentication during user login.

from django.db import models # Gives access to Django ORM which contains all DB fields like CharField, etc

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mobilizer', 'Mobilizer'),
        ('counsellor', 'Counsellor'),
        ('teacher', 'Teacher'),
        ('trainee', 'Trainee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

ROLE_CHOICES = (
    ('user', 'U'),
    ('company', 'C')
)

# Create your models here.
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField()
    photo = models.ImageField(upload_to='users/images/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)

    
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

ROLE_CHOICES = (
    ('U', 'user'),
    ('O', 'offerer')
)

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField()
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='U')
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    
    def __str__(self):
        if self.first_name == '' and self.last_name == '':
            return f'{self.username}'
        return f'{self.first_name} {self.last_name}'
    
    
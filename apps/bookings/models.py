import uuid
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Base(models.Model):
    status = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    deleted = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Service(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    image_1 = models.ImageField(upload_to='photos/')
    image_2 = models.ImageField(upload_to='photos/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='photos/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='photos/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='photos/', blank=True, null=True)


class Housing(Base):
    user = models.ForeignKey(User, related_name='housings', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    photos = models.OneToOneField(Photo, related_name='housings', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, related_name='housings', blank=True)
    capacity = models.PositiveIntegerField()
    pets = models.BooleanField(default=True)
    price_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


STATUS_BOOKING = (
    ('C', 'confirmed'),
    ('P', 'pending'),
    ('R', 'rejected'),
    ('IP', 'inprogress')
)

class Booking(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    housing = models.ForeignKey(Housing, related_name='bookings', on_delete=models.CASCADE)
    start_booking = models.DateTimeField()
    end_booking = models.DateTimeField()
    status_booking = models.CharField(choices=STATUS_BOOKING, max_length=2, default='P')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f'{self.housing} por {self.user.username}'


class Comment(Base):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    housing = models.ForeignKey(Housing, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    score = models.FloatField()

    def __str__(self):
        return f'De {self.user.username} a {self.housing.name}'

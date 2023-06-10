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



class Hotel(Base):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    description = models.TextField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='bookings/images/')
    services = models.CharField(max_length=250)


class Room(Base):
    number = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    price_day = models.PositiveIntegerField()
    description = models.TextField()


STATUS_BOOKING = (
    ('confirmed', 'C'),
    ('pending', 'P'),
    ('rejected', 'R'),
    ('inprogress', 'IP'),
)

class Booking(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_booking = models.DateTimeField()
    end_booking = models.DateTimeField()
    number_guests = models.PositiveIntegerField()
    status_booking = models.CharField(choices=STATUS_BOOKING, max_length=10)


class Comment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.FloatField()

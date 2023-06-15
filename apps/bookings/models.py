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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=150)
    description = models.TextField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='bookings/images/')
    services = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Room(Base):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()
    price_day = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    description = models.TextField()

    def __str__(self):
        return self.number


STATUS_BOOKING = (
    ('C', 'confirmed'),
    ('P', 'pending'),
    ('R', 'rejected'),
    ('IP', 'inprogress')
)

class Booking(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_booking = models.DateTimeField()
    end_booking = models.DateTimeField()
    status_booking = models.CharField(choices=STATUS_BOOKING, max_length=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return self.id


class Comment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.FloatField()

    def __str__(self):
        return self.content

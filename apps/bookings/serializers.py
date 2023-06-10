from rest_framework import serializers
from .models import Hotel, Booking, Room, Comment

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ('status', 'created', 'updated', 'deleted')
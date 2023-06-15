from rest_framework import serializers
from .models import Hotel, Booking, Room, Comment

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ('status', 'created', 'updated', 'deleted')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ('status', 'created', 'updated', 'deleted')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('status', 'created', 'updated', 'deleted')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('status', 'created', 'updated', 'deleted')
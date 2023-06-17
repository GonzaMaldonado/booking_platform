from datetime import datetime
from rest_framework import serializers
from .models import Hotel, Booking, Room, Comment

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ('status', 'created', 'updated', 'deleted')

    def to_representation(self, instance):
        return {
            'user': instance.user.username,
            'name': instance.name,
            'address': instance.address,
            'description': instance.description if instance.description != '' else '',
            'photo': instance.photo.url,
            'services': instance.services
        }


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ('status', 'created', 'updated', 'deleted')


    def validate(self, attrs):
        now = datetime.now()
        if attrs['start_booking'] < now and attrs['end_booking'] < now:
            raise serializers.ValidationError('La fecha no puede establecerse en tiempo pasado')
        return attrs
    


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('status', 'created', 'updated', 'deleted')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('status', 'created', 'updated', 'deleted')
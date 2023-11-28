from datetime import datetime
import pytz
from rest_framework import serializers
from .models import Housing, Booking, Comment

class HousingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        exclude = ('status', 'created', 'updated', 'deleted')

    """ def to_representation(self, instance):
        return {
            'user': instance.user.username,
            'name': instance.name,
            'address': instance.address,
            'description': instance.description if instance.description != '' else '',
            'photo': instance.photo.url,
            'services': instance.services
        } """


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ('status', 'created', 'updated', 'deleted')


    def validate(self, attrs):
        now = datetime.now(pytz.utc)
        start_booking = attrs['start_booking'].replace(tzinfo=pytz.utc)
        end_booking = attrs['end_booking'].replace(tzinfo=pytz.utc)
        if start_booking < now and end_booking < now:
            raise serializers.ValidationError('La fecha no puede establecerse en tiempo pasado')
        return attrs
    


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('status', 'created', 'updated', 'deleted')
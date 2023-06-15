from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import RolePermission

from .serializers import HotelSerializer, BookingSerializer, RoomSerializer, CommentSerializer
from .models import Hotel, Booking, Room, Comment


class HotelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RolePermission]
    serializer_class = HotelSerializer
    queryset = Hotel.objects.filter(status=True)


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.filter(status=True)

    def create(self, request, *args, **kwargs):
        booking = request.data
        duracion = booking['end_booking'] - booking['start_booking']
        num_noches = duracion.days
        booking['total_price'] = request.data['room']['price_day'] * num_noches
        booking['status_booking'] = 'P'
        booking_serializer = self.serializer_class(data=booking)
        reserva_existente = Booking.objects.filter(
            Q(start_booking__lte=booking['start_booking']) & Q(end_booking__gte=booking['end_booking'])
        )
        if reserva_existente.exists():
            return Response({'La habitación esta reservada para el rango de fecha dado.'})
        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response({
                'message': 'Booking created successfully',
                'booking': booking_serializer.data,
            },status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Ocurrio un error en la reserva',
            'error': booking_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)



class RoomviewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RolePermission]
    serializer_class = RoomSerializer
    queryset = Room.objects.filter(status=True)


    def filter_queryset(self, queryset):
        start_booking = self.request.query_params.get('start_booking')
        end_booking = self.request.query_params.get('end_booking')
        max_price = self.request.query_params.get('max_price')
        min_price = self.request.query_params.get('min_price')

        if start_booking and end_booking:
            queryset = queryset.filter(
                Q(booking__start_booking__lt=start_booking, booking__end_booking__gt=start_booking) &
                Q(booking__start_booking__lt=end_booking, booking__end_booking__gt=end_booking) 
            )

        if max_price and min_price:
            queryset = queryset.filter(price_day__gte=min_price, room__price_day__lte=max_price)

        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(status=True)
    
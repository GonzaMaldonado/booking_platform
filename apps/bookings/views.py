from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import RolePermission

from .serializers import HotelSerializer, BookingSerializer, RoomSerializer, CommentSerializer
from .models import Hotel, Booking, Room, Comment

# gonza6 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2ODkxNTAyLCJpYXQiOjE2ODY4NjI3MDIsImp0aSI6ImM4ZDNlNmE4MDgwNjQ3ZmFiNjFlNzM2ODUxYTkzMDFhIiwidXNlcl9pZCI6MX0.6YyFuDwoBWJsSxbRUEL3ph4rFAG7aUq-oJAWLmlTllg
# maldo eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2ODkxNTc0LCJpYXQiOjE2ODY4NjI3NzQsImp0aSI6IjJjZGQ4ODM3MzA5NjRmMTViZGQ0ZjQxMzFlZGY4YWZkIiwidXNlcl9pZCI6NH0.-4VohsEyJHumM4YEYHBYnZb4AuWPjzBqVJYKdblK4nk

class HotelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RolePermission]
    serializer_class = HotelSerializer


    def get_object(self):
        """
            Obtengo el objeto llamando a super().get_object()
            Verifico que el usuario que esta haciendo la consulta sea el que creo el objeto
            En caso contrario devuelvo una respuesta de permiso denegado
        """
        hotel = super().get_object()

        if hotel.user != self.request.user:
            self.permission_denied(self.request)

        return hotel


    def get_queryset(self):
        return Hotel.objects.filter(status=True, user=self.request.user)

    
    def create(self, request, *args, **kwargs):
        hotel = self.serializer_class(data=request.data)
        if hotel.is_valid():
            hotel.save()
            return Response({
                'message': 'Hotel creado correctamente.',
                'hotel': hotel.data
            }, status=status.HTTP_201_CREATED)
        return Response({
                'message': 'Existen errores en el registro.',
                'error': hotel.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    # Para que cuando se cree un hotel se le asigne el usuario que esta haciendo la peticion
    #def perform_create(self, serializer):
     #   serializer.save(user=self.request.user)



class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    

    def get_object(self):
        booking = super().get_object()

        if booking.user != self.request.user:
            self.permission_denied(self.request)

        return booking


    def get_queryset(self):
        return Booking.objects.filter(status=True, user=self.request.user)
    

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
                'message': 'Reserva creada exitosamente.',
                'booking': booking_serializer.data,
            },status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Ocurrio un error en la reserva',
            'error': booking_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)



class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RolePermission]
    serializer_class = RoomSerializer


    def get_object(self):
        room = super().get_object()

        if room.hotel.user != self.request.user:
            self.permission_denied(self.request)

        return room
    

    def get_queryset(self):
        return Room.objects.filter(status=True, hotel__user=self.request.user)


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

    def get_object(self):
        comment = super().get_object()

        if comment.user != self.request.user:
            self.permission_denied(self.request)

        return comment
    
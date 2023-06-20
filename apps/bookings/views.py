from datetime import datetime
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .permissions import RolePermission

from .serializers import HotelSerializer, BookingSerializer, RoomSerializer, CommentSerializer
from .models import Hotel, Booking, Room, Comment

# g6 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDU0MDYxLCJpYXQiOjE2ODcwMjUyNjEsImp0aSI6ImFiYzFlNmY5ZWE1NDQ0ZWY5MjhhZTkzNWI2YmNlYTRjIiwidXNlcl9pZCI6MX0.w6q2mw_0s_D0n2TP857Qqvpd-U8HvhK7nwya3OwMBoc
# m eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDUzNTE5LCJpYXQiOjE2ODcwMjQ3MTksImp0aSI6IjBmZjZiYmFkZGI4NjQ5ZjA4YmNiMWRmNGI0YWQ3YmFkIiwidXNlcl9pZCI6NH0.oZwopJ7ztArwIdi9Xe2Mx7RSE2HSO5Dq61lPemzs9Ng

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
        """
        Para que un usuario pueda obtener una lista solo de sus hoteles
        """
        return Hotel.objects.filter(status=True, user=self.request.user)
    
    @action(methods=['get'], detail=False)
    def get_all_hotels(self, request):
        self.permission_classes = [IsAuthenticated]
        hotels = Hotel.objects.filter(status=True)
        serializer = self.serializer_class(hotels, many=True)
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        # Hago una copia del data para agregar el user asociado
        data = request.data.copy()
        data['user'] = request.user.id

        hotel = self.serializer_class(data=data)
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
        booking = request.data.copy()
        room = Room.objects.filter(id=request.data['room']).first()

        datetime1 = datetime.strptime(booking['start_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
        datetime2 = datetime.strptime(booking['end_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
        num_noches = abs((datetime1 - datetime2).days)

        booking['total_price'] = room.price_day * num_noches
        booking['status_booking'] = 'P'
        booking['user'] = request.user.id
        
        reserva_existente = Booking.objects.filter(
            Q(start_booking__lte=booking['start_booking']) & Q(end_booking__gte=booking['end_booking']) & Q(room__exact=booking['room'])
        )
        if reserva_existente.exists():
            return Response({'error': 'La habitación esta reservada para el rango de fecha dado.'},status=status.HTTP_400_BAD_REQUEST)
        
        booking_serializer = self.serializer_class(data=booking)
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
        booking = request.data.copy()

        booking['user'] = request.user.id
        
        if 'room' in request.data:
            room = Room.objects.filter(id=request.data['room']).first()
  

        if 'start_booking' in request.data and 'end_booking' in request.data:
            datetime1 = datetime.strptime(booking['start_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
            datetime2 = datetime.strptime(booking['end_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
            num_noches = abs((datetime1 - datetime2).days)

            booking['total_price'] = room.price_day * num_noches
            
            reserva_existente = Booking.objects.filter(
                Q(start_booking__lte=booking['start_booking']) & Q(end_booking__gte=booking['end_booking']) & Q(room=booking['room'])
            ).first()
            
            if reserva_existente is not None and reserva_existente.user != request.user:
                return Response({'error': 'La habitación ya esta reservada para el rango de fecha dado.'},status=status.HTTP_400_BAD_REQUEST)
        
        booking_serializer = self.serializer_class(instance=self.get_object(), data=booking)
        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response({
                'message': 'Reserva actualizada exitosamente.',
                'booking': booking_serializer.data,
            })
        return Response({
            'message': 'Ocurrio un error en la actualización de la reserva',
            'error': booking_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



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
    
    @action(methods=['get'], detail=False)
    def get_all_rooms(self, request):
        self.permission_classes = [IsAuthenticated]
        room = Room.objects.filter(status=True).order_by('hotel')
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        #Comprobar que el usuario que crea la habitación sea el propietario del hotel
        hotels = Hotel.objects.filter(status=True, user=request.user)
        hotels = list(hotels)

        if len(hotels) == 0:
            return Response({'error': 'Debe tener un hotel antes de crear habitaciones'}, status=status.HTTP_400_BAD_REQUEST)
        
        for hotel in hotels:
            room = self.serializer_class(data=request.data)
            if room.is_valid():
                if int(hotel.id) == int(request.data['hotel']):
                    room.save()
                    return Response({
                        'message': 'Habitación creada correctamente',
                        'room': room.data
                    }, status=status.HTTP_201_CREATED)
                
                return Response({'error': 'No puede crear habitaciones que no pertenezcan a su hotel'},
                                status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                'message': 'Exiten errores en el registro',
                'error': room.errors
            }, status=status.HTTP_400_BAD_REQUEST)
                    
        

    def update(self, request, *args, **kwargs):
        hotels = Hotel.objects.filter(status=True, user=request.user)
        hotels = list(hotels)
    
        for hotel in hotels:
            room = self.serializer_class(instance=self.get_object(), data=request.data)
            if room.is_valid():
                if int(hotel.id) == int(request.data['hotel']):
                    room.save()
                    return Response({
                        'message': 'Habitación actualizada correctamente',
                        'room': room.data
                    })
                    
                return Response({'error': 'No puede actualizar habitaciones que no pertenezcan a su hotel'},
                                status=status.HTTP_401_UNAUTHORIZED)
                
            return Response({
                'message': 'Exiten errores en el registro',
                'error': room.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
    


    def filter_queryset(self, queryset):
        #start_booking = self.request.query_params.get('start_booking')
        #end_booking = self.request.query_params.get('end_booking') creo que esto va en booking
        max_price = self.request.query_params.get('max_price')
        min_price = self.request.query_params.get('min_price')

        #if start_booking and end_booking:
         #   queryset = queryset.filter(
          #      Q(booking__start_booking__lt=start_booking, booking__end_booking__gt=start_booking) &
           #     Q(booking__start_booking__lt=end_booking, booking__end_booking__gt=end_booking) 
            #)

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
    
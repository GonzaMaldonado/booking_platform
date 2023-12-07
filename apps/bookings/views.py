from datetime import datetime
from django.db.models import Q

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import RolePermission

from .serializers import HousingSerializer, BookingSerializer, CommentSerializer, ServiceSerializer
from .models import Housing, Booking, Comment, Photo, Service

# g6 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDU0MDYxLCJpYXQiOjE2ODcwMjUyNjEsImp0aSI6ImFiYzFlNmY5ZWE1NDQ0ZWY5MjhhZTkzNWI2YmNlYTRjIiwidXNlcl9pZCI6MX0.w6q2mw_0s_D0n2TP857Qqvpd-U8HvhK7nwya3OwMBoc
# m eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDUzNTE5LCJpYXQiOjE2ODcwMjQ3MTksImp0aSI6IjBmZjZiYmFkZGI4NjQ5ZjA4YmNiMWRmNGI0YWQ3YmFkIiwidXNlcl9pZCI6NH0.oZwopJ7ztArwIdi9Xe2Mx7RSE2HSO5Dq61lPemzs9Ng

class HousingListView(generics.ListAPIView):
    """
        Para que cualquier usuario obtenga una lista de alojamientos
    """
    serializer_class = HousingSerializer

    def get_queryset(self):
        queryset = Housing.objects.all()
        for housing in queryset:
            photos = Photo.objects.get(id=housing.photos.id)
            print(photos, '\n', housing)
        return queryset


class HousingDetailView(generics.RetrieveAPIView):
    """
        Para que cualquier usuario obtenga una alojamiento en específico
    """
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        housing = super().get_object()
        photos = Photo.objects.get(id=housing.photos.id)
        return housing
    


class HousingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RolePermission]
    serializer_class = HousingSerializer

    def get_object(self):
        """
            Obtengo el objeto llamando a super().get_object()
            Verifico que el usuario que esta haciendo la consulta sea el que creo el objeto
            En caso contrario devuelvo una respuesta de permiso denegado
        """
        housing = super().get_object()

        if housing.user != self.request.user:
            self.permission_denied(self.request)

        return housing


    def get_queryset(self):
        """
        Para que un usuario pueda obtener una lista de sus alojamientos
        """
        return Housing.objects.filter(status=True, user=self.request.user)

    
    def create(self, request, *args, **kwargs):
        # Hago una copia del data para agregar el user asociado
        data = request.data.copy()
        data['user'] = request.user.id
    
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')
        image_3 = request.FILES.get('image_3')
        image_4 = request.FILES.get('image_4')
        image_5 = request.FILES.get('image_5')

        photos = Photo.objects.create(image_1=image_1, image_2=image_2, image_3=image_3, image_4=image_4, image_5=image_5)
        data['photos'] = photos.id

        housing = self.serializer_class(data=data)
        if housing.is_valid():
            housing.save()
            return Response({
                'message': 'Alojamiento creado correctamente.',
                'housing': housing.data
            }, status=status.HTTP_201_CREATED)
        
        photos.delete()
        return Response({
                'message': 'Existen errores en el registro.',
                'error': housing.errors
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
            queryset = queryset.filter(price_day__gte=min_price, price_day__lte=max_price)

        return queryset



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
        housing = Housing.objects.filter(id=request.data['housing']).first()

        datetime1 = datetime.strptime(booking['start_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
        datetime2 = datetime.strptime(booking['end_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
        num_noches = abs((datetime1 - datetime2).days)

        booking['total_price'] = housing.price_day * num_noches
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
        
        if 'housing' in request.data:
            housing = Housing.objects.filter(id=request.data['housing']).first()
  

        if 'start_booking' in request.data and 'end_booking' in request.data:
            datetime1 = datetime.strptime(booking['start_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
            datetime2 = datetime.strptime(booking['end_booking'], '%Y-%m-%dT%H:%M:%S.%fZ')
            num_noches = abs((datetime1 - datetime2).days)

            booking['total_price'] = housing.price_day * num_noches
            
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



class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(status=True)

    def get_object(self):
        comment = super().get_object()

        if comment.user != self.request.user:
            self.permission_denied(self.request)

        return comment
    

class ServicesListView(generics.ListAPIView):
    """
        Para obtener una lista de servicios
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

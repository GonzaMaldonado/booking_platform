from django.contrib import admin
from .models import Hotel, Booking, Room, Comment
from apps.users.models import User


class HotelAdmin(admin.ModelAdmin):

    # Devolver Hoteles relacionados con el usuario
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Hotel.objects.all()
        else:
            return Hotel.objects.filter(user=request.user)

    # Devolver nombre de usuario relacionado con el usuario autenticado
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (request.user.is_superuser) and (db_field.name == "user"):
            kwargs['queryset'] = User.objects.filter(is_staff=1)
        else:
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class RoomAdmin(admin.ModelAdmin):

    # Devolver Hoteles relacionados con el usuario
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Room.objects.all()
        else:
            return Room.objects.filter(hotel__user=request.user)




admin.site.register(Hotel, HotelAdmin)
admin.site.register(Booking)
admin.site.register(Room, RoomAdmin)
admin.site.register(Comment)
from django.contrib import admin
from .models import Housing, Booking, Comment, Photo, Service
from apps.users.models import User


class HousingAdmin(admin.ModelAdmin):

    # Devolver Housinges relacionados con el usuario
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Housing.objects.all()
        else:
            return Housing.objects.filter(user=request.user)

    # Devolver nombre de usuario relacionado con el usuario autenticado
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (request.user.is_superuser) and (db_field.name == "user"):
            kwargs['queryset'] = User.objects.filter(is_staff=1)
        else:
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Housing, HousingAdmin)
admin.site.register(Booking)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Service)
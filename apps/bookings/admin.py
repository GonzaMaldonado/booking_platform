from django.contrib import admin
from .models import Hotel, Booking, Room, Comment

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Comment)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, BookingViewSet, RoomViewSet, CommentViewSet

router = DefaultRouter()

router.register(r'boooking', BookingViewSet, basename='booking')
router.register(r'hotel', HotelViewSet, basename='hotel')
router.register(r'room', RoomViewSet, basename='room')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls))
]
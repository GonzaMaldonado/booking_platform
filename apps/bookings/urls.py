from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HousingViewSet, BookingViewSet, CommentViewSet

router = DefaultRouter()

router.register(r'housing', HousingViewSet, basename='housing')
router.register(r'booking', BookingViewSet, basename='booking')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls))
]
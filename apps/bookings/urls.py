from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  HousingListView, HousingDetailView, HousingViewSet, BookingViewSet, CommentViewSet

router = DefaultRouter()

router.register(r'housing', HousingViewSet, basename='housing')
router.register(r'booking', BookingViewSet, basename='booking')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('get_all_housings/', HousingListView.as_view()),
    path('get_housing/<int:id>/', HousingDetailView.as_view()),
    path('', include(router.urls))
]
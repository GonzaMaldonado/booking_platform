from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Login, Logout, UserViewSet, UserModelViewSet

router = DefaultRouter()
router.register(r'', UserModelViewSet, basename='users')

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', include(router.urls)),
]
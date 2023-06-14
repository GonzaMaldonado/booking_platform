from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Register, Login, Logout, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', include(router.urls)),
]
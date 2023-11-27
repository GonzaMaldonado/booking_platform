from django.contrib.auth import authenticate

from rest_framework import status, viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, RegisterSerializer
from .models import User



class Register(views.APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            login_serializer = TokenObtainPairSerializer(data=request.data)
            if login_serializer.is_valid():
                return Response({
                    'access': login_serializer.validated_data.get('access'),
                    'refresh': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Usuario creado correctamente'
                })
        return Response({'message': 'Existen errores en el registro', 'error': user_serializer.errors
                         },status=status.HTTP_400_BAD_REQUEST)



class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'access': login_serializer.validated_data.get('access'),
                    'refresh': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesión exitoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Username o contraseña invalido'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Username o contraseña incorrecto'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0))

        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)
        return Response({'message': 'Credenciales invalidas'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    
    def create(self, request, *args, **kwargs):
        pass


    def destroy(self, request, pk=None):
        user = User.objects.filter(id=pk).update(is_active=False)
        if user == 1:
            return Response({'detail': 'Usuario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
       
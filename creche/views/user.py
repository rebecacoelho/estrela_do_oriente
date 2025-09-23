from ..serializer import UserSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Registro de usuários normais
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
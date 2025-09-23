from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Diretor
from ..serializer import  DiretorSerializer


class DiretorViewSet(viewsets.ModelViewSet):
    queryset = Diretor.objects.all()
    serializer_class = DiretorSerializer
    permission_classes = [IsAuthenticated]
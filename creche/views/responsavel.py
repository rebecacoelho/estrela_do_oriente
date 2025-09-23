from rest_framework import viewsets
from ..models.responsavel import Responsavel
from ..serializer import ResponsavelSerializer

class ResponsavelViewSet(viewsets.ModelViewSet):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
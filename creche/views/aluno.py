from rest_framework import viewsets
from ..models.aluno import Aluno
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsDiretor
from ..serializer import AlunoSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema
class AlunoViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Aluno.objects.all()

    @extend_schema(
        request=AlunoSerializer,
        responses={201: AlunoSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated & IsDiretor]
from rest_framework import viewsets
from ..models.aluno import Aluno
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsDiretor
from ..serializer import AlunoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated & IsDiretor]
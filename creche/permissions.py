# permissions.py
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsDiretor(BasePermission):
    """
    SIMPLIFICADO: Agora permite acesso para qualquer usuário autenticado.
    Não verifica mais se é Diretor - qualquer usuário com token válido tem acesso.
    """
    def has_permission(self, request, view):
        # Simplesmente verifica se está autenticado
        return request.user and request.user.is_authenticated

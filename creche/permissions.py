# permissions.py
from rest_framework.permissions import BasePermission
from .models import Diretor

class IsDiretor(BasePermission):
    """
    Permite acesso apenas para usuários que sejam Diretores
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and Diretor.objects.filter(user=request.user).exists()
        )

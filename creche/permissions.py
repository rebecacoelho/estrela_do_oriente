# permissions.py
from rest_framework.permissions import BasePermission
from .models import Diretor

class IsDiretor(BasePermission):
    """
    Permite acesso apenas para usuários que sejam Diretores
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if hasattr(request.user,'is_director'):
            return request.user.is_director
        is_director = Diretor.objects.filter(user=request.user).exists()
        request.user.is_director = is_director
        return is_director

from django.db import models
from django.contrib.auth.models import User

class Diretor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='diretor')  # vincula ao usuário Django
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diretor: {self.user.username}"
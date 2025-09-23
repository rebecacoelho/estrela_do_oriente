from django.db import models


class Responsavel(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, blank=False, null=False)
    telefone = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    endereco = models.TextField(blank=False, null=False)
    dados_extra = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Responsável {self.nome} com email: {self.email}"

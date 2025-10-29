from django.db import models


class Responsavel(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, blank=False, null=False)
    # Campos temporariamente opcionais até executar migrations
    rg = models.CharField(max_length=15, blank=True, null=True, default='')
    telefone = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    endereco = models.TextField(blank=False, null=False)
    local_de_trabalho = models.CharField(max_length=255, blank=True, null=True, default='')
    dados_extra = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Responsável {self.nome} com email: {self.email}"

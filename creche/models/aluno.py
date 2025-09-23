from django.db import models
from .responsavel import Responsavel

class Aluno(models.Model):
    GENEROS = [
        ("masc","Masculino"),
        ("fem","Feminino"),
    ]
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=50,choices=GENEROS)
    matricula = models.CharField(max_length=50, null=True, blank=True)
    responsaveis = models.ManyToManyField(Responsavel, related_name="alunos")
    criado_em = models.DateTimeField(auto_now_add=True)
    turma = models.CharField(max_length=100, blank=True, null=True)
    renda_familiar_mensal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    comprovante_residencia_url = models.FileField(
        upload_to="documentos/residencial/"
    )  # link para storage
    ativo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.matricula:
            count = 0
            self.matricula = f"MAT-{count+1:05d}"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Aluno {self.nome}, matricula: {self.matricula}"

from django.db import models


class Documento(models.Model):
    TIPOS = [
        ("residencia", "Comprovante de Residência"),
        ("renda", "Comprovante de Renda"),
        ("identidade", "Documento de Identidade"),
        ("outro", "Outro"),
    ]
    aluno = models.ForeignKey(
        "creche.Aluno",
        on_delete=models.CASCADE,
        related_name="documentos",
        null=True,
        blank=True,
    )
    tipo = models.CharField(max_length=50, choices=TIPOS)
    arquivo = models.FileField(
        upload_to="documentos/outros/",
        null=True,
        blank=True
    )  # armazenar URL do object storage
    baixado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.aluno.nome if self.aluno else "Sem aluno vinculado"}"

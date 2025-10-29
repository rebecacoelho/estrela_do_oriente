from django.db import models
from django.utils.translation import gettext_lazy as _

class PessoaAutorizada(models.Model):
    # Relacionamento One-to-Many
    aluno = models.ForeignKey(
        'Aluno',
        on_delete=models.CASCADE,
        related_name='autorizados_retirada', # Nome reverso para o Aluno
        verbose_name=_('Aluno')
    )
    
    nome = models.CharField(max_length=255, verbose_name=_('Nome'))
    parentesco = models.CharField(max_length=50, verbose_name=_('Parentesco'))
    rg = models.CharField(max_length=20, verbose_name=_('RG'))
    fone = models.CharField(max_length=20, verbose_name=_('Telefone'))
    
    # Campo opcional para registrar se esta pessoa é um dos Responsáveis (para auditoria)
    e_responsavel_legal = models.BooleanField(
        default=False, 
        verbose_name=_('É Responsável Legal Cadastrado')
    )

    class Meta:
        verbose_name = _("Pessoa Autorizada para Retirada")
        verbose_name_plural = _("Pessoas Autorizadas para Retirada")

    def __str__(self):
        return f"{self.nome} ({self.parentesco}) - Autorizado para {self.aluno.nome}"
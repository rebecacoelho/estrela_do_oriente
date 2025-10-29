from django.db import models
from django.utils.translation import gettext_lazy as _

class Endereco(models.Model):
    aluno = models.OneToOneField(
        'Aluno',
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("Aluno"),
    )
    logradouro = models.CharField(max_length=255, verbose_name=_('Endereço'))
    numero = models.CharField(max_length=10, verbose_name=_('Número'))        # NÚMERO:
    ponto_referencia = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name=_('Ponto de Referência')  # PONTO DE REFERÊNCIA:
    )
    bairro = models.CharField(max_length=100, verbose_name=_('Bairro'))      # BAIRRO:
    municipio = models.CharField(max_length=100, verbose_name=_('Município')) # MUNICÍPIO:
    uf = models.CharField(max_length=2, verbose_name=_('UF'))                # UF:
    cep = models.CharField(max_length=9, verbose_name=_('CEP'))              # CEP:
    
    class Meta:
        verbose_name = _("Endereço da Criança")
        verbose_name_plural = _("Endereços das Crianças")
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.municipio}/{self.uf}"
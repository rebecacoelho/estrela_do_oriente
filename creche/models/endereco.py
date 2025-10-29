from django.db import models
from django.utils.translation import gettext_lazy as _

class Endereco(models.Model):
    """
    MODELO COMPATÍVEL COM SCHEMA ANTIGO
    Usado tanto para Responsavel quanto para Aluno (relacionamento separado)
    """
    # Campos do schema antigo
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(blank=True, max_length=255, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)  # No schema antigo era cidade, não municipio
    estado = models.CharField(max_length=2)    # No schema antigo era estado, não uf
    
    # Campos adicionais para compatibilidade com uso atual
    @property
    def municipio(self):
        return self.cidade
    
    @property
    def uf(self):
        return self.estado
    
    @property
    def ponto_referencia(self):
        return self.complemento
    
    class Meta:
        db_table = 'creche_endereco'  # Garante que usa a tabela correta
        verbose_name = _("Endereço")
        verbose_name_plural = _("Endereços")
    
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"


class EnderecoAluno(models.Model):
    """
    Relacionamento específico Aluno-Endereco (OneToOne)
    Mantido para compatibilidade com serializers de Aluno
    """
    aluno = models.OneToOneField(
        'Aluno',
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("Aluno"),
        related_name='endereco_aluno'
    )
    logradouro = models.CharField(max_length=255, verbose_name=_('Endereço'))
    numero = models.CharField(max_length=10, verbose_name=_('Número'))
    ponto_referencia = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name=_('Ponto de Referência')
    )
    bairro = models.CharField(max_length=100, verbose_name=_('Bairro'))
    municipio = models.CharField(max_length=100, verbose_name=_('Município'))
    uf = models.CharField(max_length=2, verbose_name=_('UF'))
    cep = models.CharField(max_length=9, verbose_name=_('CEP'))
    
    class Meta:
        db_table = 'creche_enderecoaluno'  # Tabela diferente
        verbose_name = _("Endereço do Aluno")
        verbose_name_plural = _("Endereços dos Alunos")
    
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.municipio}/{self.uf}"
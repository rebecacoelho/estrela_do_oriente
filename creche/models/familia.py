from django.db import models
from django.utils.translation import gettext_lazy as _

class MembroFamiliar(models.Model):
    # Relacionamento One-to-Many: Um Aluno pode ter Múltiplos Membros Familiares
    aluno = models.ForeignKey(
        'Aluno', 
        on_delete=models.CASCADE,
        related_name='composicao_familiar', # Usado para acessar a lista (ex: aluno.composicao_familiar.all())
        verbose_name=_('Aluno Matrícula'),
    )

    # --- CAMPOS DA TABELA ---
    
    nome = models.CharField(
        max_length=255, 
        verbose_name=_('Nome Completo'), # Nome de todos os componentes...
    )
    
    idade = models.PositiveSmallIntegerField(
        verbose_name=_('Idade'),
    )
    
    # Campo para a coluna "Grau de Parentesco" (coluna fina não nomeada na imagem, mas essencial)
    parentesco = models.CharField(
        max_length=50, 
        verbose_name=_('Grau de Parentesco'),
        help_text=_('Ex: Mãe, Pai, Irmão, Avó, Próprio Aluno.'),
    )

    situacao_escolar = models.CharField(
        max_length=255,
        verbose_name=_('Situação Escolar'), # até que séries estudou ou estuda
        blank=True,
        null=True,
    )
    
    situacao_emprego = models.CharField(
        max_length=255,
        verbose_name=_('Situação de Emprego'), # o que faz
        blank=True,
        null=True,
    )
    
    renda_bruta = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name=_('Salários / Aposentadorias / Pensões e Outros (Valor Bruto R$)'),
    )

    class Meta:
        verbose_name = _("Membro Familiar")
        verbose_name_plural = _("Membros Familiares")
        # Pode ser útil ordenar pelo grau de parentesco ou idade no admin
        ordering = ['-renda_bruta', 'idade'] 

    def __str__(self):
        return f"{self.nome} ({self.parentesco}) - Família {self.aluno.nome}"
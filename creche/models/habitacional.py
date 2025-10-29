from django.db import models
from django.utils.translation import gettext_lazy as _

class SituacaoHabitacional(models.Model):
    # --- CHOICES DE TIPOS DE MORADIA ---
    TIPO_IMOVEL_CHOICES = [
        ('propria', _('CASA PRÓPRIA')),
        ('cedida', _('CASA CEDIDA')),
        ('alugada', _('CASA ALUGADA')),
    ]
    
    # --- CHOICES DE PISO ---
    TIPO_PISO_CHOICES = [
        ('cimento', _('PISO DE CIMENTO')),
        ('lajota', _('PISO DE LAJOTA')),
        ('chao_batido', _('PISO DE CHÃO BATIDO')),
    ]

    # --- CHOICES DE COBERTURA ---
    TIPO_COBERTURA_CHOICES = [
        ('tijolo', _('TIJOLO')),
        ('taipa', _('TAIPA')),
        ('madeira', _('MADEIRA')),
        ('telha', _('COBERTURA DE TELHA')),
        ('zinco', _('COBERTURA DE ZINCO')),
        ('palha', _('COBERTURA DE PALHA')),
    ]


    # Relação One-to-One com o Aluno
    aluno = models.OneToOneField(
        'Aluno', 
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('Aluno'),
    )

    # --- SITUAÇÃO HABITACIONAL ---
    
    # É um campo de escolha única (Radio Buttons na imagem)
    tipo_imovel = models.CharField(
        max_length=10,
        choices=TIPO_IMOVEL_CHOICES,
        verbose_name=_('Tipo de Imóvel'),
    )
    
    valor_aluguel = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Valor do Aluguel (R$)'),
    )
    
    numero_comodos = models.PositiveSmallIntegerField(
        verbose_name=_('Nº de Cômodos'),
    )

    # --- ESTRUTURA (Piso e Cobertura) ---
    
    piso_cimento = models.BooleanField(default=False, verbose_name=_('Piso de Cimento'))
    piso_lajota = models.BooleanField(default=False, verbose_name=_('Piso de Lajota'))
    piso_chao_batido = models.BooleanField(default=False, verbose_name=_('Piso de Chão Batido'))
    
    
    # JSONField é o mais flexível aqui:
    tipo_moradia_estrutura = models.JSONField(
        default=list,
        verbose_name=_('Estrutura de Moradia (Paredes/Cobertura)'),
    )

    # --- SANEAMENTO E CONDIÇÕES ---
    
    saneamento_fossa = models.BooleanField(default=False, verbose_name=_('Fossa'))
    saneamento_cifon = models.BooleanField(default=False, verbose_name=_('Cifon'))
    energia_eletrica = models.BooleanField(default=False, verbose_name=_('Energia Elétrica'))
    agua_encanada = models.BooleanField(default=False, verbose_name=_('Água Encanada'))
    
    class Meta:
        verbose_name = _("Situação Habitacional e Sanitária")
        verbose_name_plural = _("Situações Habitacionais e Sanitárias")

    def __str__(self):
        return f"Situação Habitacional do Aluno {self.aluno.nome}"
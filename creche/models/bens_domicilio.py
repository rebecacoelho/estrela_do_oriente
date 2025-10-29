from django.db import models
from django.utils.translation import gettext_lazy as _

class BensDomicilio(models.Model):
    # Relação One-to-One com o Aluno
    aluno = models.OneToOneField(
        'Aluno', 
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('Aluno'),
    )

    # Coluna 1:
    tv = models.BooleanField(default=False, verbose_name=_('TV'))
    dvd = models.BooleanField(default=False, verbose_name=_('DVD'))
    radio = models.BooleanField(default=False, verbose_name=_('Rádio'))
    computador = models.BooleanField(default=False, verbose_name=_('Computador'))
    notebook = models.BooleanField(default=False, verbose_name=_('Notebook'))

    # Coluna 2:
    telefone_fixo = models.BooleanField(default=False, verbose_name=_('Telefone Fixo'))
    telefone_celular = models.BooleanField(default=False, verbose_name=_('Telefone Celular'))
    tablet = models.BooleanField(default=False, verbose_name=_('Tablet'))
    internet = models.BooleanField(default=False, verbose_name=_('Internet'))
    tv_assinatura = models.BooleanField(default=False, verbose_name=_('TV por Assinatura'))

    # Coluna 3:
    fogao = models.BooleanField(default=False, verbose_name=_('Fogão'))
    geladeira = models.BooleanField(default=False, verbose_name=_('Geladeira'))
    freezer = models.BooleanField(default=False, verbose_name=_('Freezer'))
    micro_ondas = models.BooleanField(default=False, verbose_name=_('Micro-Ondas'))
    maquina_lavar_roupa = models.BooleanField(default=False, verbose_name=_('Máquina de Lavar Roupa'))

    # Coluna 4:
    ar_condicionado = models.BooleanField(default=False, verbose_name=_('Ar Condicionado'))
    bicicleta = models.BooleanField(default=False, verbose_name=_('Bicicleta'))
    moto = models.BooleanField(default=False, verbose_name=_('Moto'))
    automovel = models.BooleanField(default=False, verbose_name=_('Automóvel'))


    class Meta:
        verbose_name = _("Bens no Domicílio")
        verbose_name_plural = _("Bens no Domicílio")

    def __str__(self):
        return f"Bens do Aluno {self.aluno.nome}"
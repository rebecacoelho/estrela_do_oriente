from django.db import models
from django.db.models import Sum
from .responsavel import Responsavel
from .endereco import Endereco
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import json
class Aluno(models.Model):
    CLASSIFICACOES_POSSIVEIS = [
    "Altas Habilidades (superdotação)",
    "Cegueira",
    "Deficiência Auditiva (surdez leve ou moderada)",
    "Deficiência Auditiva (surdez severa ou profunda)",
    "Deficiência Auditiva (processamento central)",
    "Deficiência Visual (baixa visão)",
    "Deficiência Física (cadeirante) - permanente",
    "Deficiência Física (paralisia cerebral)",
    "Deficiência Física (paraplegia ou monoplegia)",
    "Deficiência Física (outros)",
    "Disfemia (gagueira)",
    "Deficiência Intelectual",
    "Sensorial Alta (sensibilidade)",
    "Sensorial Baixa (sensibilidade)",
    "Deficiência mental",
    "Espectro Autista Nível I",
    "Espectro Autista Nível II",
    "Espectro Autista Nível III",
    "Estrabismo",
    "Surdo",
    "Síndrome de Down",
    "TEA", 
    "TDAH",
    "TOD",
    ]
    GENEROS = [
        ("masc", _("Masculino")),
        ("fem", _("Feminino")),
    ]
    COR = [
        ('branca', _("Branca")),
        ('parda', _("Pardo")),
        ('negra', _("Negra")),
    ]
    MOBILIDADE_REDUZIDA = [
        ('temp', _("TEMPORÁRIA")),
        ('perm', _("PERMANENTE"))
    ]
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=50,choices=GENEROS)
    raca = models.CharField(max_length=25,choices=COR)
    gemeos = models.CharField(max_length=255,null=True,blank=True)
    irmao_na_creche = models.BooleanField(default=False,null=True,blank=True)
    cadastro_nacional_de_saude = models.CharField(max_length=15)
    unidade_de_saude = models.CharField(max_length=100)  # Aumentado para aceitar nomes completos
    problemas_de_saude = models.BooleanField(default=False,null=True,blank=True)
    restricao_alimentar = models.TextField(blank=True,null=True)
    alergia = models.TextField(blank=True,null=True)
    deficiencias_multiplas = models.TextField(blank=True,null=True)
    mobilidade_reduzida = models.CharField(max_length=25,blank=True,choices=MOBILIDADE_REDUZIDA,null=True)
    crianca_alvo_educacao_especial = models.TextField(null=True,blank=True)
    classificacoes = models.JSONField(default=list,blank=True,verbose_name=_('Classificações Especiais'))
    responsavel_recebe_auxilio = models.TextField()
    telefone = models.CharField(max_length=20, blank=False, null=False)
    matricula = models.CharField(max_length=50, null=True, blank=True)
    responsaveis = models.ManyToManyField(Responsavel, related_name="alunos")
    criado_em = models.DateTimeField(auto_now_add=True)
    turma = models.CharField(max_length=100, blank=True, null=True)
    renda_familiar_mensal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    comprovante_residencia_url = models.FileField(
        upload_to="documentos/residencial/",null=True,blank=True
    )  # link para storage
    certidao_nascimento = models.FileField(
        upload_to="documentos/certidoes/",null=True,blank=True
    )
    ativo = models.BooleanField(default=True)
    serie_cursar = models.CharField(
        max_length=100, 
        verbose_name=_('Série que irá cursar'), 
        blank=True, 
        null=True
    )
    ano_cursar = models.CharField(
        max_length=4, 
        verbose_name=_('Ano de Início'),
        help_text=_('Ex: 2025'),
        blank=True, 
        null=True
    )

    @property
    def renda_familiar_total(self):
        """Calcula a soma das rendas de todos os membros familires relacionados."""
        return self.composicao_familiar.aggregate(total=Sum('renda_bruta'))['total'] or 0.00
    
    @property
    def renda_per_capta(self):
        """Calcula a renda total dividida pelo número de membros da família."""
        total = self.renda_familiar_total
        num_membros = self.composicao_familiar.count()

        if num_membros > 0:
            return total / num_membros
        return 0.00
    
    def clean(self):
        super().clean()
        
        if isinstance(self.classificacoes, str):
            try:
                self.classificacoes = json.loads(self.classificacoes)
            except Exception:
                self.classificacoes = [self.classificacoes]

    # if not isinstance(self.classificacoes, list):
    #     raise ValidationError({'classificacoes': ['O campo de classificações deve ser uma lista.']})
    #     if not isinstance(self.classificacoes,list):
    #         raise ValidationError(
    #             {'classificacoes': _('O campo de classificações deve ser uma lista.')}
    #         )
        for c in self.classificacoes:
            if c not in self.CLASSIFICACOES_POSSIVEIS:
                raise ValidationError(
                    {'classificacoes': _(f"A classificação '{c}' não é um valor permitido.")}
                )
                
    
    def save(self, *args, **kwargs):
        from django.db.models import Max
        self.clean()
        if not self.matricula:
            last_number = Aluno.objects.aggregate(max_num=Max('id'))['max_num'] or 0
            self.matricula = f"MAT-{last_number +1:05d}"
        return super().save(*args, **kwargs)

    def get_endereco(self):
        try:
            return self.endereco
        except Endereco.DoesNotExist as e:
            return f"Esse endereço não existe: {e}"
    def __str__(self):
        return f"Aluno {self.nome}, matricula: {self.matricula}"
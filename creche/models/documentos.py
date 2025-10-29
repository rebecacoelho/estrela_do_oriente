from django.db import models
from django.utils.translation import gettext_lazy as _

class DocumentosAluno(models.Model):
    # Relacionamento One-to-One: o PK (primary_key=True) cria a relação
    aluno = models.OneToOneField(
        'Aluno', 
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('Aluno'),
    )

    # --- CAMPOS DA CERTIDÃO DE NASCIMENTO ---
    
    certidao_nascimento_matricula = models.CharField(
        max_length=50, 
        verbose_name=_('Matrícula da Certidão de Nascimento') # CERTIDÃO DE NASCIMENTO Nr Matrícula:
    )
    municipio_nascimento = models.CharField(
        max_length=100, 
        verbose_name=_('Município do Nascimento') # MUNICÍPIO DO NASCIMENTO:
    )
    municipio_registro = models.CharField(
        max_length=100, 
        verbose_name=_('Município do Registro') # MUNICÍPIO DO REGISTRO:
    )
    cartorio_registro = models.CharField(
        max_length=255, 
        verbose_name=_('Cartório de Registro') # CARTÓRIO DE REGISTRO:
    )
    
    # Campo para o ARQUIVO da certidão
    arquivo_certidao = models.FileField(
        upload_to="documentos/certidoes/", 
        blank=True, 
        null=True,
        verbose_name=_('Arquivo da Certidão (PDF/Imagem)') 
    )

    # --- CAMPOS DE RG / CPF ---
    
    # CPF
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        blank=False, 
        null=False,
        verbose_name=_('CPF') # CPF:
    )
    
    # RG
    rg = models.CharField(
        max_length=20, 
        blank=False, 
        null=False, 
        verbose_name=_('RG') # RG:
    )
    data_emissao_rg = models.DateField(
        blank=False, 
        null=False, 
        verbose_name=_('Data de Emissão do RG') # DATA DE EMISSÃO:
    )
    orgao_emissor_rg = models.CharField(
        max_length=50, 
        blank=False, 
        null=False, 
        verbose_name=_('Órgão Emissor do RG') # ÓRGÃO EMISSOR:
    )
    
    class Meta:
        verbose_name = _("Documentos da Criança")
        verbose_name_plural = _("Documentos das Crianças")

    def __str__(self):
        return f"Documentos do Aluno {self.aluno.nome}"
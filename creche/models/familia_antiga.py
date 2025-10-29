from django.db import models

class Familia(models.Model):
    """
    MODELO STUB PARA COMPATIBILIDADE COM BANCO ANTIGO
    Este modelo existia na migration inicial mas não é usado na estrutura atual.
    Mantido apenas para evitar erros de ForeignKey.
    """
    renda_familiar = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    beneficio_social = models.BooleanField(default=False)
    tipo_beneficio = models.CharField(blank=True, max_length=100, null=True)
    bens_domicilio = models.OneToOneField('BensDomicilio', on_delete=models.CASCADE, null=True, blank=True)
    habitacional = models.OneToOneField('SituacaoHabitacional', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'creche_familia'
    
    def __str__(self):
        return f"Familia - Renda: {self.renda_familiar}"


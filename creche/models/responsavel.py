from django.db import models


class Responsavel(models.Model):
    """
    MODELO ADAPTADO PARA COMPATIBILIDADE COM BANCO DE DADOS ANTIGO
    Mantém os campos da migration inicial para evitar erros.
    """
    # Campos básicos (compatível com schema antigo)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    data_nascimento = models.DateField(null=True, blank=True)  # Opcional temporariamente
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    profissao = models.CharField(max_length=100, blank=True, null=True, default='')
    local_trabalho = models.CharField(max_length=200, blank=True, null=True)
    renda_mensal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    
    # Relacionamentos (compatível com schema antigo)
    endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, null=True, blank=True)
    familia = models.ForeignKey('Familia', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Responsável {self.nome} com email: {self.email}"
    
    class Meta:
        db_table = 'creche_responsavel'  # Garante que usa a tabela correta

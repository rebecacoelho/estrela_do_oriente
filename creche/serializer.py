from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from .models import (
    Aluno,
    Documento,
    Responsavel,
    Endereco,
    DocumentosAluno,
    SituacaoHabitacional,
    BensDomicilio,
    MembroFamiliar,
    PessoaAutorizada
)
from .models.diretor import Diretor
import json

class PessoaAutorizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaAutorizada
        exclude = ('aluno',)
class MembroFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembroFamiliar
        exclude = ('aluno',)
class BensDomicilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = BensDomicilio
        exclude = ('aluno',)
class SituacaoHabitacionalSerializer(serializers.ModelSerializer):
    choices = [c[0] for c in (SituacaoHabitacional.TIPO_PISO_CHOICES + SituacaoHabitacional.TIPO_COBERTURA_CHOICES + SituacaoHabitacional.TIPO_IMOVEL_CHOICES)]
    tipo_moradia_estrutura = serializers.ListField(
        child=serializers.ChoiceField(choices=choices),
        allow_empty=True
    )

    class Meta:
        model = SituacaoHabitacional
        exclude = ('aluno',)
class DocumentosAlunoSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(
        max_length=14,
        allow_blank=False,
        required=True
    )
    class Meta:
        model = DocumentosAluno
        exclude = ('aluno',)
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        exclude = ('aluno',)
class AlunoSerializer(serializers.ModelSerializer):
    
    endereco = EnderecoSerializer()
    documentosaluno = DocumentosAlunoSerializer()
    situacaohabitacional = SituacaoHabitacionalSerializer()
    bensdomicilio = BensDomicilioSerializer()
    composicao_familiar = MembroFamiliarSerializer(many=True)
    autorizados_retirada = PessoaAutorizadaSerializer(many=True)

    comprovante_residencia_url = serializers.FileField(required=False,allow_null=True)
    renda_familiar_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    renda_per_capta = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    classificacoes = serializers.MultipleChoiceField(
        choices=Aluno.CLASSIFICACOES_POSSIVEIS,
        allow_empty=True
    )
    responsaveis = serializers.PrimaryKeyRelatedField(many=True,queryset=Responsavel.objects.all())
    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "raca",
            "classificacoes",
            "endereco",
            "documentosaluno",
            "cadastro_nacional_de_saude",
            "unidade_de_saude",
            "problemas_de_saude",
            "situacaohabitacional",
            "bensdomicilio",
            "composicao_familiar",
            "autorizados_retirada",
            "matricula",
            "data_nascimento",
            "genero",
            "responsaveis",
            "criado_em",
            "turma",
            "renda_familiar_mensal",
            "comprovante_residencia_url",
            "renda_familiar_total", 
            "renda_per_capta", 
            "ativo",
        ]
        read_only_fields = [
            "id",
            "criado_em",
            "matricula",
            "renda_familiar_total", 
            "renda_per_capta", 
        ]

    def to_representation(self, instance):
        """
        Garante que o campo 'classificacoes' (ou qualquer campo que possa 
        se tornar um set) seja uma lista para ser serializável em JSON.
        """
        # Chama a implementação padrão para obter os dados serializados
        data = super().to_representation(instance)
        
        # 💡 CONVERSÃO OBRIGATÓRIA AQUI:
        if 'classificacoes' in data and isinstance(data['classificacoes'], set):
            data['classificacoes'] = list(data['classificacoes'])
            
        # 💡 (Opcional) Faça o mesmo para 'responsaveis' se não usar o PrimaryKeyRelatedField
        # Se você usar o PrimaryKeyRelatedField, esta linha não será necessária.
        if 'responsaveis' in data and isinstance(data['responsaveis'], set):
            data['responsaveis'] = list(data['responsaveis'])
            
        return data
    def to_internal_value(self, data):
        mutable_data = data.copy()

        # Converte strings JSON para listas reais
        for field in ['composicao_familiar', 'autorizados_retirada', 'classificacoes']:
            if field in mutable_data and isinstance(mutable_data[field], str):
                try:
                    mutable_data[field] = json.loads(mutable_data[field])
                except json.JSONDecodeError:
                    # Pode vir como 'TEA,Cegueira'
                    if ',' in mutable_data[field]:
                        mutable_data[field] = [x.strip() for x in mutable_data[field].split(',')]
                    else:
                        mutable_data[field] = [mutable_data[field]]

        return super().to_internal_value(mutable_data)
    def get_renda_familiar_total(self, obj):
        return obj.renda_familiar_total  # chama a propriedade do modelo

    def get_renda_per_capta(self, obj):
        return obj.renda_per_capta  # chama a propriedade do modelo
    def create(self, validated_data):
        documentos_data = validated_data.pop('documentosaluno')
        endereco_data = validated_data.pop('endereco')
        habitacional_data = validated_data.pop('situacaohabitacional')
        bens_data = validated_data.pop('bensdomicilio')
        familia_data = validated_data.pop('composicao_familiar')
        autorizados_retirada_data = validated_data.pop('autorizados_retirada')
        responsaveis_data = validated_data.pop('responsaveis', [])
        classificacoes_data = validated_data.pop('classificacoes', [])
        if isinstance(classificacoes_data, set):
            classificacoes_data = list(classificacoes_data)
        aluno = Aluno.objects.create(**validated_data)
       
        DocumentosAluno.objects.create(aluno=aluno,**documentos_data)
        Endereco.objects.create(aluno=aluno,**endereco_data)
        SituacaoHabitacional.objects.create(aluno=aluno,**habitacional_data)
        BensDomicilio.objects.create(aluno=aluno,**bens_data)
        membros = [MembroFamiliar(aluno=aluno, **item) for item in familia_data]
        MembroFamiliar.objects.bulk_create(membros)
        autorizados = [PessoaAutorizada(aluno=aluno,**item) for item in autorizados_retirada_data]
        PessoaAutorizada.objects.bulk_create(autorizados)
        if classificacoes_data:
            aluno.classificacoes = classificacoes_data
            aluno.save(update_fields=['classificacoes'])
        if responsaveis_data:
            aluno.responsaveis.set(responsaveis_data)
        return aluno
    
    @transaction.atomic
    def update(self, instance, validated_data):
        # Atualiza campos diretos
        endereco_data = validated_data.pop('endereco', None)
        documentos_data = validated_data.pop('documentosaluno', None)
        situacao_habitacional_data = validated_data.pop('situacaohabitacional', None)
        bens_data = validated_data.pop('bensdomicilio', None)
        familiares_data = validated_data.pop('composicao_familiar', [])
        autorizados_data = validated_data.pop('autorizados_retirada', [])

        # Atualiza campos simples do Aluno
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualizações OneToOne (create ou update)
        if endereco_data:
            Endereco.objects.update_or_create(aluno=instance, defaults=endereco_data)
        if documentos_data:
            DocumentosAluno.objects.update_or_create(aluno=instance, defaults=documentos_data)
        if situacao_habitacional_data:
            SituacaoHabitacional.objects.update_or_create(aluno=instance, defaults=situacao_habitacional_data)
        if bens_data:
            BensDomicilio.objects.update_or_create(aluno=instance, defaults=bens_data)

        # Atualizações OneToMany com bulk ops
        def bulk_update_related(model, related_name, data):
            related_manager = getattr(instance, related_name)
            existing_items = {item.id: item for item in related_manager.all()}
            update_list, create_list, keep_ids = [], [], []

            for item_data in data:
                item_id = item_data.pop('id', None)
                if item_id and item_id in existing_items:
                    item = existing_items[item_id]
                    for field, value in item_data.items():
                        setattr(item, field, value)
                    update_list.append(item)
                    keep_ids.append(item_id)
                else:
                    create_list.append(model(aluno=instance, **item_data))

            # Deletar os que não foram mantidos
            to_delete = [obj for obj_id, obj in existing_items.items() if obj_id not in keep_ids]
            if to_delete:
                model.objects.filter(id__in=[obj.id for obj in to_delete]).delete()

            # Execução em massa
            if update_list:
                model.objects.bulk_update(update_list, fields=[f.name for f in model._meta.fields if f.name not in ['id', 'aluno']])
            if create_list:
                model.objects.bulk_create(create_list)

        bulk_update_related(MembroFamiliar, 'composicao_familiar', familiares_data)
        bulk_update_related(PessoaAutorizada, 'autorizados_retirada', autorizados_data)

        return instance
class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = [
            "id",
            "aluno",
            "tipo",
            "arquivo",
            "baixado_em",
        ]
        read_only_fields = ["id", "baixado_em"]


class ResponsavelSerializer(serializers.ModelSerializer):
    # Campo endereco_texto para receber string do frontend
    endereco_texto = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    # Campos opcionais
    rg = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')
    local_trabalho = serializers.CharField(max_length=200, required=False, allow_blank=True)
    profissao = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    data_nascimento = serializers.DateField(required=False, allow_null=True)
    renda_mensal = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True, default=0)
    
    class Meta:
        model = Responsavel
        fields = ["id", "nome", "cpf", "rg", "data_nascimento", "telefone", "email", "profissao", 
                  "local_trabalho", "renda_mensal", "endereco", "endereco_texto"]
        read_only_fields = ["id", "endereco"]
    
    def create(self, validated_data):
        # Se veio endereco_texto, cria um objeto Endereco primeiro
        endereco_texto = validated_data.pop('endereco_texto', None)
        
        if endereco_texto:
            # Cria um endereço simplificado compatível com schema antigo
            endereco_obj = Endereco.objects.create(
                logradouro=endereco_texto[:255],
                numero='S/N',
                bairro='',
                cidade='',  # campo do schema antigo
                estado='',  # campo do schema antigo
                cep='',
                complemento=''
            )
            validated_data['endereco'] = endereco_obj
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Se veio endereco_texto, atualiza o endereço
        endereco_texto = validated_data.pop('endereco_texto', None)
        
        if endereco_texto:
            if instance.endereco:
                instance.endereco.logradouro = endereco_texto[:255]
                instance.endereco.save()
            else:
                endereco_obj = Endereco.objects.create(
                    logradouro=endereco_texto[:255],
                    numero='S/N',
                    bairro='',
                    cidade='',  # campo do schema antigo
                    estado='',  # campo do schema antigo
                    cep='',
                    complemento=''
                )
                validated_data['endereco'] = endereco_obj
        
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )

class DiretorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diretor
        fields = ["id", "user", "criado_em"]
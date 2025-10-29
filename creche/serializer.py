from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from .models import (
    Aluno,
    Documento,
    Responsavel,
    Endereco,
    EnderecoAluno,
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
        model = EnderecoAluno
        exclude = ('aluno',)
class AlunoSerializer(serializers.ModelSerializer):
    
    endereco = EnderecoSerializer(source='endereco_aluno')
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
            "data_nascimento",
            "genero",
            "raca",
            "gemeos",
            "irmao_na_creche",
            "cadastro_nacional_de_saude",
            "unidade_de_saude",
            "problemas_de_saude",
            "restricao_alimentar",
            "alergia",
            "deficiencias_multiplas",
            "mobilidade_reduzida",
            "crianca_alvo_educacao_especial",
            "classificacoes",
            "responsavel_recebe_auxilio",
            "telefone",
            "endereco",
            "documentosaluno",
            "situacaohabitacional",
            "bensdomicilio",
            "composicao_familiar",
            "autorizados_retirada",
            "matricula",
            "responsaveis",
            "criado_em",
            "turma",
            "renda_familiar_mensal",
            "comprovante_residencia_url",
            "certidao_nascimento",
            "renda_familiar_total", 
            "renda_per_capta", 
            "ativo",
            "serie_cursar",
            "ano_cursar",
            "status_matricula",
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
        Customiza a saída para:
        1. Converter 'classificacoes' de set para lista
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
        # Torna mutável se for QueryDict do Django
        if hasattr(data, '_mutable'):
            data._mutable = True
        
        # Converte para dict padrão do Python (QueryDict causa problemas)
        if hasattr(data, 'dict'):
            # QueryDict.dict() retorna um dict Python normal, mas perde listas
            # Precisamos processar manualmente
            regular_dict = {}
            for key in data.keys():
                values = data.getlist(key)  # Pega todos os valores para essa chave
                if len(values) == 1:
                    regular_dict[key] = values[0]
                else:
                    regular_dict[key] = values  # Mantém como lista se houver múltiplos
            data = regular_dict
        else:
            data = dict(data)
        
        # DEBUG com print (sempre aparece no Gunicorn)
        print("\n" + "=" * 60)
        print("🔍 ALUNO SERIALIZER - DADOS RECEBIDOS (primeiros 15 campos):")
        for i, key in enumerate(list(data.keys())[:15]):
            print(f"  {key} = {repr(data[key])[:100]}")
        print("=" * 60 + "\n")
        
        # Processa campos com notação de ponto (ex: endereco.logradouro)
        nested_objects = {}
        keys_to_remove = []
        
        for key in list(data.keys()):
            if '.' in key:
                parent, child = key.split('.', 1)
                if parent not in nested_objects:
                    nested_objects[parent] = {}
                
                value = data[key]
                
                # Converte valores booleanos, números e null
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                elif value == 'null' or value == '':
                    value = None
                elif isinstance(value, str):
                    # Tenta converter números (incluindo floats)
                    try:
                        if '.' in value and value.replace('.', '').replace('-', '').isdigit():
                            value = float(value)
                        elif value.isdigit():
                            value = int(value)
                    except:
                        pass  # Mantém como string
                    
                nested_objects[parent][child] = value
                keys_to_remove.append(key)
        
        # DEBUG: Mostra objetos reconstruídos
        print("\n🔧 OBJETOS ANINHADOS RECONSTRUÍDOS:")
        for parent, obj in nested_objects.items():
            print(f"  {parent}: {obj}")
        print("=" * 60 + "\n")
        
        # Remove chaves com ponto
        for key in keys_to_remove:
            del data[key]
        
        # Adiciona objetos reconstruídos
        for parent, obj in nested_objects.items():
            data[parent] = obj

        # Converte strings JSON para listas/objetos reais
        json_fields = ['composicao_familiar', 'autorizados_retirada']
        
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                    print(f"✅ {field}: parseado de JSON string")
                except json.JSONDecodeError as e:
                    print(f"❌ {field}: ERRO ao parsear JSON - {e}")
        
        # Converte responsaveis de string para lista
        if 'responsaveis' in data and isinstance(data['responsaveis'], str):
            data['responsaveis'] = [int(data['responsaveis'])]
            print(f"✅ responsaveis: convertido de string '{data['responsaveis'][0]}' para lista")
        
        # Converte tipo_moradia_estrutura de string para lista (dentro de situacaohabitacional)
        if 'situacaohabitacional' in data and isinstance(data['situacaohabitacional'], dict):
            if 'tipo_moradia_estrutura' in data['situacaohabitacional']:
                valor = data['situacaohabitacional']['tipo_moradia_estrutura']
                if isinstance(valor, str):
                    data['situacaohabitacional']['tipo_moradia_estrutura'] = [valor]
                    print(f"✅ situacaohabitacional.tipo_moradia_estrutura: convertido de string para lista")

        print("\n📦 DADOS FINAIS ANTES DA VALIDAÇÃO DRF:")
        print(f"  - endereco: {data.get('endereco', 'AUSENTE')}")
        print(f"  - documentosaluno: {data.get('documentosaluno', 'AUSENTE')}")
        print(f"  - situacaohabitacional: {data.get('situacaohabitacional', 'AUSENTE')}")
        print(f"  - bensdomicilio: {data.get('bensdomicilio', 'AUSENTE')}")
        print(f"  - composicao_familiar: {data.get('composicao_familiar', 'AUSENTE')}")
        print(f"  - autorizados_retirada: {data.get('autorizados_retirada', 'AUSENTE')}")
        print(f"  - responsaveis: {data.get('responsaveis', 'AUSENTE')}")
        print("=" * 60 + "\n")
        
        try:
            result = super().to_internal_value(data)
            print("✅ VALIDAÇÃO DRF PASSOU!\n")
            return result
        except Exception as e:
            print(f"❌ ERRO NA VALIDAÇÃO DRF: {e}\n")
            raise
    
    def get_renda_familiar_total(self, obj):
        return obj.renda_familiar_total  # chama a propriedade do modelo

    def get_renda_per_capta(self, obj):
        return obj.renda_per_capta  # chama a propriedade do modelo
    
    def create(self, validated_data):
        documentos_data = validated_data.pop('documentosaluno')
        endereco_data = validated_data.pop('endereco_aluno')
        habitacional_data = validated_data.pop('situacaohabitacional')
        bens_data = validated_data.pop('bensdomicilio')
        familia_data = validated_data.pop('composicao_familiar')
        autorizados_retirada_data = validated_data.pop('autorizados_retirada')
        responsaveis_data = validated_data.pop('responsaveis', [])
        classificacoes_data = validated_data.pop('classificacoes', [])
        if isinstance(classificacoes_data, set):
            classificacoes_data = list(classificacoes_data)
        
        print(f"🔨 Criando aluno com dados: {list(validated_data.keys())}")
        aluno = Aluno.objects.create(**validated_data)
       
        DocumentosAluno.objects.create(aluno=aluno, **documentos_data)
        EnderecoAluno.objects.create(aluno=aluno, **endereco_data)
        SituacaoHabitacional.objects.create(aluno=aluno, **habitacional_data)
        BensDomicilio.objects.create(aluno=aluno, **bens_data)
        membros = [MembroFamiliar(aluno=aluno, **item) for item in familia_data]
        MembroFamiliar.objects.bulk_create(membros)
        autorizados = [PessoaAutorizada(aluno=aluno, **item) for item in autorizados_retirada_data]
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
        endereco_data = validated_data.pop('endereco_aluno', None)
        documentos_data = validated_data.pop('documentosaluno', None)
        situacao_habitacional_data = validated_data.pop('situacaohabitacional', None)
        bens_data = validated_data.pop('bensdomicilio', None)
        familiares_data = validated_data.pop('composicao_familiar', [])
        autorizados_data = validated_data.pop('autorizados_retirada', [])
        responsaveis_data = validated_data.pop('responsaveis', None)

        # Atualiza campos simples do Aluno
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualiza ManyToMany de responsaveis
        if responsaveis_data is not None:
            instance.responsaveis.set(responsaveis_data)

        # Atualizações OneToOne (create ou update)
        if endereco_data:
            EnderecoAluno.objects.update_or_create(aluno=instance, defaults=endereco_data)
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
        from datetime import date
        
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
        
        # Garante valores padrão para campos NOT NULL no banco antigo
        if 'data_nascimento' not in validated_data or validated_data['data_nascimento'] is None:
            validated_data['data_nascimento'] = date(1900, 1, 1)  # Data padrão placeholder
        
        if 'rg' not in validated_data or not validated_data['rg']:
            validated_data['rg'] = 'Não informado'
        
        if 'profissao' not in validated_data or not validated_data['profissao']:
            validated_data['profissao'] = 'Não informado'
        
        if 'renda_mensal' not in validated_data or validated_data['renda_mensal'] is None:
            validated_data['renda_mensal'] = 0.00
        
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
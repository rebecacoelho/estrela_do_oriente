from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Aluno, Documento, Responsavel
from .models.diretor import Diretor


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "matricula",
            "data_nascimento",
            "genero",
            "responsaveis",
            "criado_em",
            "turma",
            "renda_familiar_mensal",
            "comprovante_residencia_url",
            "ativo",
        ]
        read_only_fields = [
            "id",
            "criado_em",
        ]


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
    class Meta:
        model = Responsavel
        fields = ["id", "nome", "cpf", "telefone", "email", "endereco", "dados_extra"]
        read_only_fields = ["id"]

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
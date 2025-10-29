#!/bin/bash

# Script para criar usuário diretor no Railway
# Execute: railway run bash criar_usuario_railway.sh

echo "=========================================="
echo "👤 Criando Usuário Diretor no Railway"
echo "=========================================="
echo ""

python manage.py shell << EOF
from django.contrib.auth.models import User
from creche.models import Diretor

# Dados do diretor
USERNAME = 'admin'
EMAIL = 'admin@creche.com'
PASSWORD = 'admin123'

print("Verificando se usuário já existe...")

# Verificar se o usuário já existe
if User.objects.filter(username=USERNAME).exists():
    print(f"⚠️  Usuário '{USERNAME}' já existe!")
    user = User.objects.get(username=USERNAME)
else:
    # Criar superusuário
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f"✅ Usuário '{USERNAME}' criado com sucesso!")

# Verificar se o diretor já existe
if hasattr(user, 'diretor'):
    print(f"⚠️  Diretor já vinculado a este usuário!")
else:
    # Criar diretor vinculado ao usuário
    diretor = Diretor.objects.create(user=user)
    print(f"✅ Diretor criado e vinculado!")

print("")
print("=" * 50)
print("✅ CONFIGURAÇÃO COMPLETA!")
print("=" * 50)
print(f"Username: {USERNAME}")
print(f"Email: {EMAIL}")
print(f"Password: {PASSWORD}")
print("")
print("Use estas credenciais para fazer login no sistema.")
print("=" * 50)
EOF

echo ""
echo "✅ Processo concluído!"
echo ""


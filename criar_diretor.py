#!/usr/bin/env python
"""
Script para criar um usuário diretor no Django.
Execute com: python manage.py shell < criar_diretor.py

Ou copie e cole no Django shell: python manage.py shell
"""

from django.contrib.auth.models import User
from creche.models.diretor import Diretor

# Dados do diretor
USERNAME = 'diretor'
EMAIL = 'diretor@creche.com'
PASSWORD = 'diretor123'  # ALTERE ISSO EM PRODUÇÃO!

print("=" * 50)
print("Criando usuário e diretor...")
print("=" * 50)

# Verificar se o usuário já existe
if User.objects.filter(username=USERNAME).exists():
    print(f"⚠️  Usuário '{USERNAME}' já existe!")
    user = User.objects.get(username=USERNAME)
    print(f"✅ Usuário encontrado: {user.username} ({user.email})")
else:
    # Criar usuário
    user = User.objects.create_user(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    user.is_staff = True  # Permitir acesso ao admin
    user.save()
    print(f"✅ Usuário criado: {user.username}")

# Verificar se o diretor já existe
if hasattr(user, 'diretor'):
    print(f"⚠️  Diretor já existe para este usuário!")
    diretor = user.diretor
    print(f"✅ Diretor encontrado: {diretor}")
else:
    # Criar diretor vinculado ao usuário
    diretor = Diretor.objects.create(user=user)
    print(f"✅ Diretor criado: {diretor}")

print("")
print("=" * 50)
print("✅ SUCESSO!")
print("=" * 50)
print(f"Username: {USERNAME}")
print(f"Email: {EMAIL}")
print(f"Password: {PASSWORD}")
print("")
print("⚠️  IMPORTANTE: Altere a senha em produção!")
print("=" * 50)


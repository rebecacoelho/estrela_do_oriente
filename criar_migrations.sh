#!/bin/bash

# Script para criar e aplicar migrations do Django
# Execute este script quando tiver acesso ao ambiente Python com Django instalado

echo "🔄 Criando novas migrations..."
python manage.py makemigrations

echo ""
echo "📋 Mostrando SQL que será executado..."
python manage.py sqlmigrate creche 0001 || echo "Migration não encontrada ainda"

echo ""
echo "✅ Aplicando migrations ao banco de dados..."
python manage.py migrate

echo ""
echo "🎉 Migrations aplicadas com sucesso!"
echo ""
echo "Próximos passos:"
echo "1. Criar um superusuário: python manage.py createsuperuser"
echo "2. Criar um diretor vinculado ao usuário (veja INSTRUCOES_MIGRATIONS.md)"


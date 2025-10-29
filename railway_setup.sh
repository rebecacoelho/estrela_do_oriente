#!/bin/bash

echo "🚀 CONFIGURAÇÃO INICIAL DO BANCO NO RAILWAY"
echo "============================================"

# Aplicar migrations
echo "📦 Aplicando migrations..."
python manage.py makemigrations
python manage.py migrate

# Criar superuser (se necessário)
echo ""
echo "✅ Migrations aplicadas com sucesso!"
echo ""
echo "Para criar um superuser, execute:"
echo "python manage.py createsuperuser"


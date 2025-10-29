#!/bin/bash

# Script executado automaticamente no deploy do Railway

echo "🚀 Iniciando deploy..."

# Cria migrations se necessário
echo "📝 Criando migrations..."
python manage.py makemigrations --noinput

# Aplica migrations
echo "🔨 Aplicando migrations no banco..."
python manage.py migrate --noinput

# Coleta arquivos estáticos (se necessário)
# python manage.py collectstatic --noinput

echo "✅ Deploy concluído!"



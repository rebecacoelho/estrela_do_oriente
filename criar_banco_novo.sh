#!/bin/bash

# Script para criar BANCO NOVO com todos os campos
# Uso: bash criar_banco_novo.sh

echo "=========================================="
echo "🎯 CRIANDO BANCO NOVO COM TODOS OS CAMPOS"
echo "=========================================="
echo ""

echo "⚠️  ATENÇÃO: Este script vai DELETAR as migrations antigas!"
echo "          Certifique-se de ter configurado um BANCO NOVO!"
echo ""
read -p "Deseja continuar? (s/N): " resposta

if [ "$resposta" != "s" ] && [ "$resposta" != "S" ]; then
    echo "❌ Operação cancelada."
    exit 1
fi

echo ""
echo "🗑️  Deletando migrations antigas..."
find creche/migrations -name "*.py" -not -name "__init__.py" -delete
find creche/migrations -name "*.pyc" -delete

echo "✅ Migrations antigas deletadas!"

echo ""
echo "📝 Criando novas migrations..."
python manage.py makemigrations

echo ""
echo "🚀 Aplicando migrations..."
python manage.py migrate

echo ""
echo "=========================================="
echo "✅ BANCO NOVO CRIADO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📋 Próximos passos:"
echo "  1. python manage.py createsuperuser"
echo "  2. Teste o cadastro de alunos no frontend"
echo ""



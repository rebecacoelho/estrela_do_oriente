# Imagem base com Python 3.12
FROM python:3.12-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o projeto
COPY . .

# Expõe a porta do container
EXPOSE 8000

# Cria script de inicialização que executa collectstatic no runtime
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
set -e

echo "🔧 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🔧 Executando migrações..."
python manage.py migrate --noinput

echo "🚀 Iniciando servidor..."
exec gunicorn setup.wsgi:application --bind 0.0.0.0:8000 --workers 4
EOF

RUN chmod +x /app/entrypoint.sh

# Comando de inicialização
CMD ["/app/entrypoint.sh"]

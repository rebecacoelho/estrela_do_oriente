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
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🔧 Coletando arquivos estáticos..."\n\
python manage.py collectstatic --noinput\n\
\n\
echo "🔍 Verificando variáveis de ambiente..."\n\
echo "DATABASE_URL: ${DATABASE_URL:-NÃO DEFINIDA}"\n\
echo "PGHOST: ${PGHOST:-NÃO DEFINIDA}"\n\
echo "PGPORT: ${PGPORT:-NÃO DEFINIDA}"\n\
echo "PGDATABASE: ${PGDATABASE:-NÃO DEFINIDA}"\n\
echo "PGUSER: ${PGUSER:-NÃO DEFINIDA}"\n\
\n\
echo "⏳ Aguardando banco de dados..."\n\
max_attempts=30\n\
attempt=0\n\
while [ $attempt -lt $max_attempts ]; do\n\
  if python manage.py migrate --check >/dev/null 2>&1; then\n\
    echo "✅ Banco de dados conectado!"\n\
    break\n\
  fi\n\
  attempt=$((attempt + 1))\n\
  echo "🔄 Tentativa $attempt/$max_attempts - Aguardando banco..."\n\
  sleep 2\n\
done\n\
\n\
if [ $attempt -eq $max_attempts ]; then\n\
  echo "❌ Não foi possível conectar ao banco após $max_attempts tentativas"\n\
  echo "🚀 Iniciando servidor sem migrações (pode causar erros)..."\n\
  exec gunicorn setup.wsgi:application --bind 0.0.0.0:8000 --workers 4\n\
fi\n\
\n\
echo "🔧 Executando migrações..."\n\
python manage.py migrate --noinput\n\
\n\
echo "🚀 Iniciando servidor..."\n\
exec gunicorn setup.wsgi:application --bind 0.0.0.0:8000 --workers 4' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Comando de inicialização
CMD ["/app/entrypoint.sh"]

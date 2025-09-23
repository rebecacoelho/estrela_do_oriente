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

# Cria script de inicialização
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Coletando arquivos estáticos..."\n\
python manage.py collectstatic --noinput\n\
\n\
if [ -z "$DATABASE_URL" ] && [ -z "$PGHOST" ]; then\n\
  echo "Iniciando servidor sem banco..."\n\
  exec gunicorn setup.wsgi:application --bind 0.0.0.0:8000 --workers 4\n\
fi\n\
\n\
echo "Conectando ao banco de dados..."\n\
max_attempts=30\n\
attempt=0\n\
while [ $attempt -lt $max_attempts ]; do\n\
  if python manage.py migrate --check >/dev/null 2>&1; then\n\
    break\n\
  fi\n\
  attempt=$((attempt + 1))\n\
  sleep 2\n\
done\n\
\n\
if [ $attempt -lt $max_attempts ]; then\n\
  echo "Executando migrações..."\n\
  python manage.py migrate --noinput\n\
fi\n\
\n\
echo "Iniciando servidor..."\n\
exec gunicorn setup.wsgi:application --bind 0.0.0.0:8000 --workers 4' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Comando de inicialização
CMD ["/app/entrypoint.sh"]

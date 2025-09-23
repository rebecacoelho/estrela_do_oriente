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
echo "🔧 Executando migrações..."\n\
python manage.py migrate --noinput\n\
\n\
echo "🚀 Iniciando servidor..."\n\
exec gunicorn setup.wsgi:application --bind 0.0.0.0:8000 --workers 4' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Comando de inicialização
CMD ["/app/entrypoint.sh"]

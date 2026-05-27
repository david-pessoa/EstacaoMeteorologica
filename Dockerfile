FROM python:3.11-slim

# Configurações básicas
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria e define o diretório de trabalho
WORKDIR /app

# Instala dependências Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o restante do projeto
COPY . /app/

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

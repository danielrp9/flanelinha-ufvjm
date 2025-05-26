FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . /app

# Instalar dependências do SO para compilar numpy, pandas, psycopg2 e outras libs
RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Criar e ativar ambiente virtual
RUN python -m venv /opt/venv

# Atualizar pip e instalar requisitos usando o pip do venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install -r requirements.txt

# Adicionar venv ao PATH para rodar binários python/pip diretamente
ENV PATH="/opt/venv/bin:$PATH"

# Expõe a porta padrão do gunicorn
EXPOSE 8000

# Comando para rodar o gunicorn com seu projeto Django
CMD ["gunicorn", "flanelinha.wsgi", "--bind", "0.0.0.0:8000"]

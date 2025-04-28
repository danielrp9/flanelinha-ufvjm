# Flanelinha WebApp

Sistema de gerenciamento de estacionamento, feito com Django desenvolvido para a disciplina de engenharia web.

## Requisitos do Projeto

- Python 3.10 ou superior
- Django 5.2
- Ambiente virtual recomendado (`venv`)
- Estrutura inicial:

## Instalação e Configuração

1. Clone o repositório:
 git clone <url-do-repositorio>
 cd flanelinha-webapp


2. Crie e Ative o ambiente virtual 
 
python -m venv venv
source venv/Scripts/activate  # Windows


3. Installe o dotenv
pip install python-dotenv

Obs.: O python-dotenv é uma biblioteca que lê variáveis de ambiente que estão em um arquivo .env

4. Aplique as migrações no banco de dados
python manage.py mikemigrations
python manage.py migrate

5. Inicie o servidor em desenvolvimento 
python manage.py runserver




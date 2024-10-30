
# Projeto Pets Amigos

Este projeto, desenvolvido em Django, é um sistema de gerenciamento para uma clínica veterinária, incluindo funcionalidades como cadastro de clientes, agendamento de consultas, gestão de pets, e mais.

## Clonando o Repositório

Comece clonando o projeto para o seu ambiente local:

```bash
git clone https://github.com/Edna-Alvarenga/Projeto_Pet.git
cd Projeto_Pet
cd app_pets_amigos
```

## Requisitos

Certifique-se de ter Python 3.x e pip instalados. Instale também o PostgreSQL.

## Instalação

1. **Instalando Django:**

   ```bash
   pip install Django
   ```


2. **Instalando Django Allauth**

   Este projeto utiliza o Django Allauth para autenticação. Para configurá-lo, instale o pacote com o comando:

   ```bash
   pip install django-allauth
   ```

## Configuração do Banco de Dados

No arquivo `settings.py`, configure o banco de dados PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pet_amigo_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Configuração para Envio de E-mail

Para habilitar o envio de e-mails no projeto, adicione no `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu_email'
EMAIL_HOST_PASSWORD = 'sua_senha'
```

> **Nota**: Recomenda-se criar variáveis de ambiente para proteger informações sensíveis.

## Executando a Aplicação

1. **Realize as migrações do banco de dados:**

   ```bash
   python manage.py makemigrations
   
   python manage.py migrate
   ```

2. **Crie um superusuário para acessar o painel administrativo:**

   ```bash
   python manage.py createsuperuser
   (Voce tambem pode criar o usuario na pagina inicial ao subir a aplicação)
   ```

3. **Inicie o servidor:**

   ```bash
   python manage.py runserver
   ```

Acesse a aplicação em [http://127.0.0.1:8000](http://127.0.0.1:8000).

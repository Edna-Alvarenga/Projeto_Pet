# core/models.py

from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf_cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)
    crmv = models.CharField(max_length=20)
    endereco = models.TextField()

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao = models.DurationField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Relacionamento com Empresa

    def __str__(self):
        return self.nome

# core/models.py
class Cliente(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o cliente ao usuário
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    telefone = models.CharField(max_length=15)
    #email = models.EmailField()
    email = models.EmailField(unique=True)  # Define o campo como único

    def __str__(self):
        return self.nome


class Pet(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relaciona o pet ao cliente
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50)
    idade = models.IntegerField()
    peso = models.FloatField()
    vacina = models.CharField(max_length=100, blank=True)
    remedios = models.CharField(max_length=100, blank=True)
    outros = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    observacoes = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Certifique-se de que o campo "valor" existe
    finalizado = models.BooleanField(default=False)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente} - {self.servico} em {self.data}"


class Pagamento(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    metodo_pagamento = models.CharField(max_length=20)  # 'dinheiro', 'pix', 'cartao'
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pagamento de {self.agendamento.servico.nome} para {self.agendamento.cliente.nome}"



# models.py
class Avaliacao(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='avaliacao')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Aqui é a relação com Cliente
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Avaliação de 1 a 5
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"Avaliação de {self.cliente.nome} para o serviço em {self.agendamento.data}"


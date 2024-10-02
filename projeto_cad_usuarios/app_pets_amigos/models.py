from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relaciona com o usuário
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Certifique-se de que este campo está presente


    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o cliente logado
    data = models.DateField()  # Data da consulta
    hora = models.TimeField()  # Hora da consulta
    motivo = models.TextField(null=True, blank=True)  # Motivo da consulta
    servico = models.CharField(
        max_length=50,
        choices=[
            ('banho', 'Banho'),
            ('banho_e_tosa', 'Banho e Tosa'),
            ('exames', 'Exames'),
            ('vacinas', 'Vacinas'),
            ('outros_servicos', 'Outros Serviços')
        ]
    )  # Novo campo de serviço
    cancelado = models.BooleanField(default=False)  # Se o agendamento foi cancelado

    def __str__(self):
        return f"{self.cliente.username} - {self.data} às {self.hora}"

class Pet(models.Model):
    TIPO_TAMANHO = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ]

    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos_pets/', null=True, blank=True)  # Requer configuração do media
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o pet ao tutor
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    idade = models.IntegerField()
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=[('macho', 'Macho'), ('femea', 'Fêmea')])
    tamanho = models.CharField(max_length=10, choices=TIPO_TAMANHO)
    vacinas = models.TextField(null=True, blank=True)  # Lista de vacinas
    remedios = models.TextField(null=True, blank=True)  # Lista de remédios
    alergias = models.TextField(null=True, blank=True)  # Informações sobre alergias
    outros = models.TextField(null=True, blank=True)  # Qualquer outra informação relevante

    def __str__(self):
        return f"{self.nome} ({self.tutor.username})"

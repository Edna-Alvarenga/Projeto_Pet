from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AgendamentoForm
from .models import Agendamento
from django.contrib.auth import authenticate, login
from django.contrib import messages  # Para exibir mensagens de erro/sucesso
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet


from django.shortcuts import render

def servicos(request):
    return render(request, 'app_pets_amigos/servicos.html')

def home(request):
    return render(request, 'app_pets_amigos/home.html')

from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import ClienteForm
from .models import Cliente, User

def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            telefone = form.cleaned_data['telefone']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            
            # Cria o usuário
            user = User.objects.create_user(username=email, email=email, password=senha)
            
            # Cria o cliente
            cliente = Cliente(nome=nome, telefone=telefone, email=email, user=user)
            cliente.save()
            
            return redirect('home')  # Redireciona para a página inicial após o cadastro
    else:
        form = ClienteForm()

    return render(request, 'app_pets_amigos/cadastro_cliente.html', {'form': form})


def cadastro_veterinario(request):
    return render(request, 'app_pets_amigos/cadastro_veterinario.html')
from django.shortcuts import render

def login_cliente(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            return redirect('painel_cliente')  # Redireciona para o painel do cliente
        else:
            messages.error(request, 'Email ou senha incorretos.')

    return render(request, 'app_pets_amigos/login_cliente.html')


from django.shortcuts import render

def login_veterinario(request):
    return render(request, 'app_pets_amigos/login_veterinario.html')

@login_required
def agendar_consulta(request):
    pets = Pet.objects.filter(tutor=request.user)  # Carrega os pets do cliente logado
    
    if request.method == 'POST':

        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.cliente = request.user
            agendamento.save()
            return redirect('consultas_cliente')  # Redireciona para a lista de consultas do cliente
    else:
        form = AgendamentoForm()
    
    return render(request, 'app_pets_amigos/agendar_consulta.html', {'form': form, 'pets': pets})

@login_required
def consultas_cliente(request):
    consultas = Agendamento.objects.filter(cliente=request.user, cancelado=False)
    return render(request, 'app_pets_amigos/consultas_cliente.html', {'consultas': consultas})

@login_required
def cancelar_consulta(request, consulta_id):
    consulta = Agendamento.objects.get(id=consulta_id, cliente=request.user)
    if consulta:
        consulta.cancelado = True
        consulta.save()
    return redirect('consultas_cliente')

@login_required
def criar_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.tutor = request.user  # Associa o pet ao usuário logado
            pet.save()
            return redirect('carteirinha_pet', pet_id=pet.id)
    else:
        form = PetForm()

    return render(request, 'app_pets_amigos/criar_pet.html', {'form': form})
@login_required
def listar_pets(request):
    pets = Pet.objects.filter(tutor=request.user)  # Mostra apenas os pets do usuário logado
    return render(request, 'app_pets_amigos/listar_pets.html', {'pets': pets})

@login_required
def editar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, tutor=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('carteirinha_pet', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    return render(request, 'app_pets_amigos/editar_pet.html', {'form': form, 'pet': pet})

@login_required
def carteirinha_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, tutor=request.user)
    return render(request, 'app_pets_amigos/carteirinha_pet.html', {'pet': pet})

# Visualizações para Home
def home(request):
    servicos = [
        {'nome': 'Banho', 'descricao': 'Serviço completo de banho para pets de todos os tamanhos com produtos específicos para cada tipo de pele.', 'icone': 'banho_icon.png'},
        {'nome': 'Banho e Tosa', 'descricao': 'Banho com tosa higiênica ou completa para manter seu pet sempre limpo e confortável.', 'icone': 'banho_tosa_icon.png'},
        {'nome': 'Exames Laboratoriais', 'descricao': 'Exames laboratoriais para diagnóstico preciso e rápido, garantindo a saúde do seu pet.', 'icone': 'exames_icon.png'},
        {'nome': 'Vermífugos', 'descricao': 'Aplicação de vermífugos para a proteção contra parasitas internos.', 'icone': 'vermifugos_icon.png'},
        {'nome': 'Cirurgias', 'descricao': 'Cirurgias realizadas por veterinários experientes com total segurança e cuidado.', 'icone': 'cirurgias_icon.png'},
        {'nome': 'Serviços Veterinários', 'descricao': 'Consultas veterinárias com profissionais qualificados para cuidar do seu pet.', 'icone': 'veterinarios_icon.png'},
        {'nome': 'Leva e Traz', 'descricao': 'Serviço de transporte especializado para levar e trazer seu pet com segurança e conforto.', 'icone': 'leva_traz_icon.png'},
    ]

    formas_pagamento = ['Pix', 'Crédito', 'Débito', 'Dinheiro']

    return render(request, 'app_pets_amigos/home.html', {'servicos': servicos, 'formas_pagamento': formas_pagamento})

@login_required
def painel_cliente(request):
    # Obtenha os dados do cliente logado
    cliente = request.user

    # Renderize o template do painel
    return render(request, 'app_pets_amigos/painel_cliente.html', {'cliente': cliente})

@login_required
def editar_cliente(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('painel_cliente')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'app_pets_amigos/editar_cliente.html', {'form': form})

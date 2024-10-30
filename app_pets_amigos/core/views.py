# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa, Servico, Cliente, Pet, Agendamento, Avaliacao
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import login
from .forms import UserRegisterForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('painel_usuario')
    else:
        form = UserRegisterForm()
    
    return render(request, 'core/cadastro_usuario.html', {'form': form})



@login_required
def painel_usuario(request):
    # Filtrar apenas os agendamentos que estão finalizados e não pagos
    agendamentos_pendentes = Agendamento.objects.filter(finalizado=True, pago=False)

    return render(request, 'core/painel_usuario.html', {'agendamentos': agendamentos_pendentes})



@login_required
def cadastrar_empresa(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        cpf_cnpj = request.POST['cpf_cnpj']
        telefone = request.POST['telefone']
        crmv = request.POST['crmv']
        endereco = request.POST['endereco']
        empresa = Empresa.objects.create(
            user=request.user,
            nome=nome,
            email=email,
            cpf_cnpj=cpf_cnpj,
            telefone=telefone,
            crmv=crmv,
            endereco=endereco,
        )
        return redirect('consultar_empresa')
    return render(request, 'core/cadastrar_empresa.html')

@login_required
def consultar_empresa(request):
    empresas = Empresa.objects.all()
    #empresas = Empresa.objects.filter(user=request.user)

    return render(request, 'core/consultar_empresa.html', {'empresas': empresas})
    

from .forms import EmpresaForm
@login_required
def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)  # Passa a empresa existente ao formulário
        if form.is_valid():
            form.save()
            return redirect('consultar_empresa')
    else:
        form = EmpresaForm(instance=empresa)  # Carrega a empresa no formulário para GET

    return render(request, 'core/editar_empresa.html', {'form': form, 'empresa': empresa})

@login_required
def excluir_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk, user=request.user)
    empresa.delete()
    return redirect('consultar_empresa')

from .models import Cliente, Servico

from datetime import datetime

@login_required
def cadastrar_servico(request):
    empresas = Empresa.objects.all()  # Carrega todas as empresas

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        duracao_str = request.POST.get('duracao')
        empresa_id = request.POST.get('empresa')  # Obtém o ID da empresa selecionada

        # Converte duracao_str para timedelta
        if duracao_str:
            try:
                horas, minutos, segundos = map(int, duracao_str.split(':'))
                duracao = timedelta(hours=horas, minutes=minutos, seconds=segundos)
            except ValueError:
                duracao = timedelta()  # Define um valor padrão se houver erro
        else:
            duracao = timedelta()

        # Converte preco para Decimal
        preco = Decimal(preco) if preco else Decimal('0.00')

        # Obtém a empresa pelo ID
        empresa = Empresa.objects.get(id=empresa_id)

        # Cria o serviço associado à empresa
        servico = Servico.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            duracao=duracao,
            empresa=empresa
        )

        return redirect('consultar_servicos')

    return render(request, 'core/cadastrar_servico.html', {'empresas': empresas})


@login_required
def consultar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'core/consultar_servicos.html', {'servicos': servicos})

from django.shortcuts import get_object_or_404, render, redirect
from .models import Servico

def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    if request.method == 'POST':
        # Lógica para atualizar o serviço
        servico.nome = request.POST.get('nome')
        servico.descricao = request.POST.get('descricao')
        servico.save()
        return redirect('consultar_servicos')

    return render(request, 'core/editar_servico.html', {'servico': servico})

def excluir_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)  # Buscar o serviço pelo ID
    if request.method == 'POST':
        servico.delete()  # Excluir o serviço
        return redirect('consultar_servicos')  # Redirecionar para a lista de serviços
    return render(request, 'core/excluir_servico.html', {'servico': servico})

from .models import Cliente, Pet
from .forms import ClienteForm, PetForm

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.user = request.user  # Associar o cliente ao usuário logado
            cliente.save()
            return redirect('consultar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'core/cadastrar_cliente.html', {'form': form})



@login_required
def cadastrar_pet(request): 
    clientes =Cliente.objects.all() # Obtenha todos clientes idependente de quem cadastrou
    #clientes = Cliente.objects.filter(user=request.user)  # Obtenha os clientes do usuário logado

    if request.method == 'POST':
        form = PetForm(request.POST)
        form.fields['cliente'].queryset = clientes  # Configure a queryset para o campo cliente

        if form.is_valid():
            pet = form.save(commit=False)
            pet.cliente = form.cleaned_data['cliente']  # Relaciona o pet ao cliente selecionado
            pet.save()
            return redirect('consultar_pets')
        else:
            # Se o formulário não for válido, exibe os erros
            return render(request, 'core/cadastrar_pet.html', {'form': form, 'clientes': clientes})
    else:
        form = PetForm()
        form.fields['cliente'].queryset = clientes  # Configure a queryset para o campo cliente

    return render(request, 'core/cadastrar_pet.html', {'form': form, 'clientes': clientes})


@login_required
def consultar_clientes(request):
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'core/consultar_clientes.html', {'clientes': clientes})

@login_required
def consultar_pets(request):
    pets = Pet.objects.filter(cliente__user=request.user)
    return render(request, 'core/consultar_pets.html', {'pets': pets})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('consultar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/editar_cliente.html', {'form': form})

@login_required
def editar_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('consultar_pets')
    else:
        form = PetForm(instance=pet)
    return render(request, 'core/editar_pet.html', {'form': form})

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, user=request.user)
    cliente.delete()
    return redirect('consultar_clientes')

@login_required
def excluir_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    pet.delete()
    return redirect('consultar_pets')

from .forms import AgendamentoForm

@login_required
def agendar_servico(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        pet_id = request.POST.get('pet')
        servico_id = request.POST.get('servico')
        data_hora = request.POST.get('data_hora')
        observacoes = request.POST.get('observacoes')

        cliente = Cliente.objects.get(id=cliente_id)
        pet = Pet.objects.get(id=pet_id)
        servico = Servico.objects.get(id=servico_id)

        # Converter data_hora para data e hora separados
        data_hora_obj = datetime.strptime(data_hora, '%Y-%m-%dT%H:%M')
        data = data_hora_obj.date()
        hora = data_hora_obj.time()

        # Criar o agendamento
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            pet=pet,
            servico=servico,
            data=data,
            hora=hora,
            valor=servico.preco,
            observacoes=observacoes,
            finalizado=False,
            pago=False
        )

        return redirect('consultar_agendamentos')

    else:
        clientes = Cliente.objects.all()
        servicos = Servico.objects.all()
        return render(request, 'core/agendar_servico.html', {'clientes': clientes, 'servicos': servicos})
# core/views.py

from django.http import JsonResponse

@login_required
def obter_valor_servico(request, servico_id):
    try:
        servico = Servico.objects.get(id=servico_id)
        return JsonResponse({'valor': str(servico.preco)})
    except Servico.DoesNotExist:
        return JsonResponse({'valor': ''}, status=404)
    
from django.http import JsonResponse

@login_required
def filtrar_pets_por_cliente(request, cliente_id):
    pets = Pet.objects.filter(cliente_id=cliente_id)
    pets_data = [{'id': pet.id, 'nome': pet.nome} for pet in pets]
    return JsonResponse({'pets': pets_data})


@login_required
def consultar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(cliente__user=request.user)
    return render(request, 'core/consultar_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk, cliente__user=request.user)
    agendamento.delete()
    return redirect('consultar_agendamentos')

@login_required
def finalizar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk, cliente__user=request.user)
    agendamento.finalizado = True
    agendamento.save()
    return redirect('consultar_agendamentos')

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Agendamento

def realizar_pagamento(request, agendamento_id):
    # Buscar o agendamento pelo ID, garantindo que ele existe
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, finalizado=True, pago=False)

    if request.method == 'POST':
        metodo_pagamento = request.POST.get('metodo_pagamento')

        # Atualizar o agendamento para indicar que está pago
        agendamento.pago = True
        agendamento.metodo_pagamento = metodo_pagamento  
        agendamento.save()

        # Redirecionar após o pagamento ser processado
        return redirect('consultar_agendamentos')

    return render(request, 'core/realizar_pagamento.html', {'agendamento': agendamento})



from django.db.models import Sum
from django.utils import timezone


@login_required
def faturamento(request):
    # Filtrar os agendamentos finalizados e pagos
    agendamentos = Agendamento.objects.filter(finalizado=True, pago=True)

    # Agrupando por empresa, dia, mês e ano
    faturamento_por_empresa_diario = agendamentos.values('servico__empresa__nome', 'data').annotate(total=Sum('valor'))
    faturamento_por_empresa_mensal = agendamentos.values('servico__empresa__nome', 'data__month').annotate(total=Sum('valor'))
    faturamento_por_empresa_anual = agendamentos.values('servico__empresa__nome', 'data__year').annotate(total=Sum('valor'))

    return render(request, 'core/faturamento.html', {
        'faturamento_por_empresa_diario': faturamento_por_empresa_diario,
        'faturamento_por_empresa_mensal': faturamento_por_empresa_mensal,
        'faturamento_por_empresa_anual': faturamento_por_empresa_anual,
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Agendamento, Avaliacao, Cliente
from .forms import AvaliacaoForm

#@login_required
def avaliar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            email_cliente = form.cleaned_data.get('email')
            
            # Busca o cliente pelo e-mail fornecido
            try:
                cliente = Cliente.objects.get(email=email_cliente)
                # Salva a avaliação
                avaliacao = form.save(commit=False)
                avaliacao.agendamento = agendamento
                avaliacao.cliente = cliente  # Atribui o cliente encontrado
                avaliacao.save()
                return redirect('consultar_avaliacoes')  # Redireciona após salvar
            except Cliente.DoesNotExist:
                form.add_error('email', 'Cliente com este e-mail não encontrado.')  # Mensagem de erro se o cliente não existir
    else:
        form = AvaliacaoForm()

    return render(request, 'core/avaliar_agendamento.html', {'form': form, 'agendamento': agendamento})


@login_required
def consultar_avaliacoes(request):
    print("Acessando consultar_avaliacoes")  # debug
    avaliacoes = Avaliacao.objects.select_related('cliente')  # Prepara a relação com o cliente
    return render(request, 'core/consultar_avaliacoes.html', {'avaliacoes': avaliacoes})

from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Cliente
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from core.models import Agendamento
from django.contrib.auth.decorators import login_required

@login_required
def enviar_avaliacao_email(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    # Montar o link de avaliação
    link_avaliacao = f"http://127.0.0.1:8000/avaliar/{agendamento_id}/"
    
    # Enviar e-mail
    send_mail(
        'Avaliação do Atendimento',
        f'Agradecemos por utilizar nossos serviços. Por favor, avalie seu atendimento aqui: {link_avaliacao}',
        'nao-responda@gmail.com',  # E-mail do remetente
        [agendamento.cliente.email],  # E-mail do destinatário (substitua pelo campo correto do cliente)
        fail_silently=False,
    )
    
    return redirect('painel_usuario')  

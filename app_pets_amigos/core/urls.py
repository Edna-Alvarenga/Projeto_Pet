# core/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar_usuario/', views.register, name='register'),
    path('', views.painel_usuario, name='painel_usuario'),
    path('empresa/cadastrar/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('empresa/consultar/', views.consultar_empresa, name='consultar_empresa'),
    path('empresa/editar/<int:pk>/', views.editar_empresa, name='editar_empresa'),
    path('empresa/excluir/<int:pk>/', views.excluir_empresa, name='excluir_empresa'),
    
    path('servico/cadastrar/', views.cadastrar_servico, name='cadastrar_servico'),
    path('servico/consultar/', views.consultar_servicos, name='consultar_servicos'),
    path('servico/editar/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('servico/excluir/<int:servico_id>/', views.excluir_servico, name='excluir_servico'),

    path('cliente/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('pet/cadastrar/', views.cadastrar_pet, name='cadastrar_pet'),
    path('clientes/', views.consultar_clientes, name='consultar_clientes'),
    path('pets/', views.consultar_pets, name='consultar_pets'),
    path('cliente/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('pet/editar/<int:pk>/', views.editar_pet, name='editar_pet'),
    path('cliente/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),
    path('pet/excluir/<int:pk>/', views.excluir_pet, name='excluir_pet'),
    
    path('servico/agendar/', views.agendar_servico, name='agendar_servico'),
    path('servico/consultar_agendamento/', views.consultar_agendamentos, name='consultar_agendamentos'),
    path('servico/cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('servico/finalizar/<int:pk>/', views.finalizar_agendamento, name='finalizar_agendamento'),

    path('servico/<int:servico_id>/valor/', views.obter_valor_servico, name='obter_valor_servico'),

    path('pagamento/<int:agendamento_id>/', views.realizar_pagamento, name='realizar_pagamento'),
    path('faturamento/', views.faturamento, name='faturamento'),

    path('cliente/<int:cliente_id>/pets/', views.filtrar_pets_por_cliente,name='filtrar_pets_por_cliente'),

    path('avaliar/<int:agendamento_id>/', views.avaliar_agendamento, name='avaliar_agendamento'),
    path('avaliacoes/', views.consultar_avaliacoes, name='consultar_avaliacoes'),

    path('enviar_avaliacao/<int:agendamento_id>/', views.enviar_avaliacao_email, name='enviar_avaliacao_email'),
]

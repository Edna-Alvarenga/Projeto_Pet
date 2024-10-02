from django.urls import path
from app_pets_amigos import views  # Importa o módulo `views` diretamente

urlpatterns = [
    path('', views.home, name='home'),  # Use `views.home` diretamente
    path('cadastro_cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('cadastro_veterinario/', views.cadastro_veterinario, name='cadastro_veterinario'),
    path('login_cliente/', views.login_cliente, name='login_cliente'),
    path('login_veterinario/', views.login_veterinario, name='login_veterinario'),
    path('agendar/', views.agendar_consulta, name='agendar_consulta'),
    path('consultas/', views.consultas_cliente, name='consultas_cliente'),
    path('cancelar/<int:consulta_id>/', views.cancelar_consulta, name='cancelar_consulta'),
    path('servicos/', views.servicos, name='servicos'),  # A URL para a página de serviços
    path('criar_pet/', views.criar_pet, name='criar_pet'),
    path('editar_pet/<int:pet_id>/', views.editar_pet, name='editar_pet'),
    path('carteirinha_pet/<int:pet_id>/', views.carteirinha_pet, name='carteirinha_pet'),
    path('pet/listar/', views.listar_pets, name='listar_pets'),
    path('painel_cliente/', views.painel_cliente, name='painel_cliente'),
    path('editar_cliente/', views.editar_cliente, name='editar_cliente'),

]

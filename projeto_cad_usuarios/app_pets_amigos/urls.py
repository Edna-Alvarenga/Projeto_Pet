from django.urls import path
from .views import agendar_consulta, consultas_cliente, cancelar_consulta, cadastro_cliente, login_cliente, cadastro_veterinario, login_veterinario,home, criar_pet, editar_pet, carteirinha_pet, listar_pets

urlpatterns = [
        path('home/', home, name='home'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('cadastro_veterinario/', cadastro_veterinario, name='cadastro_veterinario'),
    path('login_cliente/', login_cliente, name='login_cliente'),
    path('login_veterinario/', login_veterinario, name='login_veterinario'),
    path('agendar/', agendar_consulta, name='agendar_consulta'),
    path('consultas/', consultas_cliente, name='consultas_cliente'),
    path('cancelar/<int:consulta_id>/', cancelar_consulta, name='cancelar_consulta'),
    path('cadastrarpet/', criar_pet, name='criar_pet'),
    path('pet/editar/<int:pet_id>/', editar_pet, name='editar_pet'),
    path('pet/carteirinha/<int:pet_id>/', carteirinha_pet, name='carteirinha_pet'),
    path('pet/listar/', listar_pets, name='listar_pets'),
    
]

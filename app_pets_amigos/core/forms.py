from django import forms
from .models import Cliente, Pet, Empresa, Avaliacao
from .models import Agendamento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'password1': 'Senha',
            'password2': 'Confirme a Senha',
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if not any(char.isdigit() for char in password):
                raise ValidationError("A senha deve conter pelo menos um número.")
            if not any(char.isalpha() for char in password):
                raise ValidationError("A senha deve conter pelo menos uma letra.")
            if not any(char in "!@#$%^&*()-_=+" for char in password):
                raise ValidationError("A senha deve conter pelo menos um caractere especial.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'email','cpf_cnpj','telefone', 'crmv', 'endereco']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco','numero','complemento', 'bairro', 'localidade', 'uf', 'telefone', 'email']


class PetForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none(), label="Cliente")  # Novo campo para selecionar o cliente

    class Meta:
        model = Pet
        fields = ['cliente', 'nome', 'especie', 'raca', 'idade', 'peso', 'vacina', 'remedios', 'outros']

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'pet', 'servico', 'data', 'hora', 'valor', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),  # Isso garantirá o formato YYYY-MM-DD
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'valor': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].widget.attrs['readonly'] = True



from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    email = forms.EmailField(
        label="E-mail do Cliente", 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Avaliacao
        fields = ['email', 'nota', 'comentario']
        labels = {
            'nota': 'Nota (1 a 5)',
            'comentario': 'Comentário',
        }
        widgets = {
            'nota': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


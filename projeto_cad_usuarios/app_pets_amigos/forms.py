from django import forms
from .models import Agendamento
from django import forms
from .models import Cliente
from django import forms
from .models import Pet
from django.contrib.auth.models import User


class ClienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")
        
        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data', 'hora', 'motivo', 'servico']  # Adicione 'servico' aqui
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'foto', 'peso', 'idade', 'raca', 'sexo', 'tamanho', 'vacinas', 'remedios', 'alergias', 'outros']
        widgets = {
            'vacinas': forms.Textarea(attrs={'rows': 3}),
            'remedios': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'outros': forms.Textarea(attrs={'rows': 3}),
        }
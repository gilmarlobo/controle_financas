from django import forms
from .models import Gasto

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descricao', 'valor']  # Removemos 'data'
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição do gasto'}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Valor do gasto'}),
        }
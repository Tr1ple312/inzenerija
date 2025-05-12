from django import forms
from testsite.models import Transaction, Category


class AddTransForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'cat']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Введите сумму'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'cat': forms.Select(attrs={'class': 'form-control'}),
        }
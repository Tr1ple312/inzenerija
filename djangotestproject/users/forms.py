from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="login", widget=forms.TextInput())
    password = forms.CharField(label="password", widget=forms.TextInput())


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'First Name',
            'last_name': 'Last name'
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords do not match')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('this email already exists')
        return email



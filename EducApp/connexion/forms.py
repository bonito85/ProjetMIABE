from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Class de connexion utilisateur
class LoginForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
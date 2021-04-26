from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models  import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    nacimiento = forms.DateField()
    gametag = forms.CharField()
    nombre = forms.CharField()
    apellido = forms.CharField()

    class Meta:
        model = User
        fields = ["username","nombre","apellido","gametag","email","nacimiento"]



        
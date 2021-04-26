from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models  import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    nacimiento = forms.DateField()
    gametag = forms.TextField()
    nombre = forms.TextField()
    apellido = forms.TextField()

    class Meta:
        model = User
        fields = ["nombre","apellido","nacimiento","gametag","email","password"]



        
from django import forms
from .models import Usuario

class PuzzlevidForm(forms.ModelForm):
    class meta:
        model = Usuario
        fields=['nombre','apellido','gameTag','email','password','creadoEn','birth']
        
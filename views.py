from django.shortcuts import render
from django.http import HttpResponse
from puzzlevid.models import Usuario, Nivel, Session, Intento

# Create your views here.
def index(request):
    return render(request,'index.html')

def juega(request):
    return render(request, 'juega.html')

def steam(request):
    return render(request, 'steam.html')

def usuarios(request, pk):

    usuarios = Usuario.objects.get(pk=pk)

    sessiones = Session.objects.filter(owner_id=usuarios.id)

    context = {

        "Usuario": usuarios,

        "session": sessiones,

    }

    return render(request, "usuarios.html", context)

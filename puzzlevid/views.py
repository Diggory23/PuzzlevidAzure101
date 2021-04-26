from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models  import User
from json import loads
from django.utils import timezone
import psycopg2
from puzzlevid.models import Usuario, Nivel, Session, Intento
from .forms import RegisterForm

# Create your views here.
def index(request):
    return render(request,'index.html')


def juega(request):
    return render(request, 'juega.html')


def iniciarSesion(request):
    return render(request, 'registration/iniciarSesion.html')


def signup(response):

    nombre=''
    apellido=''
    gametag=''
    email=''
    password=''
    creadoEn= timezone.now()
    birth=''
    

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            nombre= form.cleaned_data.get("nombre")
            apellido= form.cleaned_data.get("apellido")
            gametag= form.cleaned_data.get("username")
            email= form.cleaned_data.get("email")
            password= form.cleaned_data.get("password")
            birth= form.cleaned_data.get("nacimiento")
            form.save()
        values_to_insert = [(nombre,apellido,gametag,email,password,creadoEn,birth)]
        print(values_to_insert)
        
        return redirect("/juega")
    else:
        form = RegisterForm()

    try:
        connection = psycopg2.connect(
            user = "admin",
            password = "ragnar",
            host = "localhost",
            port = "5432",
            database = "puzzlevid"
        )

        #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
        cursor = connection.cursor()
        #Display the PostgreSQL version installed
        cursor.execute("""
    INSERT INTO puzzlevid_usuario ('nombre', 'apellido','gametag','email','password','creadoEn','birth')
    VALUES (?, ?, ?, ?, ?, ?, ?)""", values_to_insert)
       
          


    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")

  
    
    
    return render(response, 'register/signup.html',{'form':form})


# def signup(request):
#     user_list= Usuario.objects.order_by('id')

#     form = PuzzlevidForm()

#     context= {'form':form}

#     return render(request, 'signup.html',context)

# @require_POST
# def addUsers(request):
#    form = PuzzlevidForm(request.POST)
    
#    if form.is_valid():
#         new_user = form.save()
        
#    return redirect('login')

@csrf_exempt
@login_required
def estadisticas(request):
    #Create a connection credentials to the PostgreSQL database
    try:
        connection = psycopg2.connect(
            user = "admin",
            password = "ragnar",
            host = "localhost",
            port = "5432",
            database = "puzzlevid"
        )

        #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
        cursor = connection.cursor()
        #Display the PostgreSQL version installed
        cursor.execute("SELECT * from puzzlevid_session;")
        rows = cursor.fetchall()
        
        #return HttpResponse(rows)
        data=[]

        for row in rows:
          retorno = {"usuarioId":row[9],
              "scoreQuimica":row[3],
              "scoreMate":row[4],
              "scoreGeografia":row[5],
              "scoreFisica":row[6],
              "scoreHistoria":row[7],
              "EnemigosEliminados":row[8]
            }
          data.append(retorno)
        print(data)
       
          


    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    '''
    
    retorno = {"usuarioId":usuario_id,
              "scoreQuimica":quimica,
              "scoreMate":mate,
              "scoreGeografia":geo,
              "scoreFisica":fisica,
              "scoreHistoria":hist,
              "EnemigosEliminados":enemigos
        }
    print(retorno)
    '''
    return render(request, 'estadisticas.html', {"data":data})
    
   

@csrf_exempt
def unity(request):
    try:
        connection = psycopg2.connect(
            user = "admin",
            password = "ragnar",
            host = "localhost",
            port = "5432",
            database = "puzzlevid"
        )

        #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
        cursor = connection.cursor()
        #Display the PostgreSQL version installed
        cursor.execute("SELECT * from puzzlevid_usuarios;")
        rows = cursor.fetchall()
        
        #return HttpResponse(rows)
        data=[]

        for row in rows:
          retorno = {
              "id":row[0],
              "nombre":row[1],
              "apellido":row[2],
              "gameTag":row[3],
              "email":row[4],
              "password":row[5],
              "creadoEn":row[6],
              "birth":row[7]
            }
          data.append(retorno)
        print(data)
       
          


    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    
    finally:
        if(connection != None):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
    '''        
    session={
        "id":1,
        "userId":1,
        "started":"2021-03-09 13:25:00",
        "ended":"2021-03-09 14:07:12",
        "scoreQuimica":8,
        "scoreMate":9,
        "scoreGeografia":7,
        "scoreFisica":8,
        "scoreHistoria":10,
        "EnemigosEliminados":7
    }
    retorno= [
        {
        "userId":"diegoisunza@gmail.com",
        "valid":"True",
        "lastSession":"2021-03-21 19:04:02"
        }
    ]
    '''
    return JsonResponse(data)

@csrf_exempt
def infoUsuario(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    user = body['data_a']
    pwd = body['data_b']
    jugador_o  = User.objects.filter(username=user)     
    jugador_objeto = Usuario.objects.filter(username=jugador_o[0].id)
    
    return HttpResponse(jugador_objeto.id)


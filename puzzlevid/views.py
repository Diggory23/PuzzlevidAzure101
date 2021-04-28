from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models  import User
from json import loads, dumps
from django.db import connection, transaction
from django.utils import timezone
import psycopg2
import hashlib
from puzzlevid.models import Usuario, Nivel, Session, Intento
from .forms import RegisterForm

# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required
def juega(request):
    return render(request, 'juega.html')


def login(request):
    return render(request, 'login.html')

@transaction.atomic
def estadisticasGlobales(request):
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
        #TODO: Cambiar usuarioId por el de la sesion
        data={}

        #Scores maximos
        cursor.execute('SELECT "usuarioId_id", sum("aciertosQuim") + sum("aciertosMate") + sum("aciertosGeo") + sum("aciertosHist") + sum("aciertosBio") as ItemSum FROM puzzlevid_session GROUP BY "usuarioId_id" ORDER BY ItemSum desc LIMIT 5;')
        top_five_scores = cursor.fetchall()
        data['top_five_scores']= top_five_scores

        #Tiempo jugado
        cursor.execute('SELECT "usuarioId_id", sum("terminoSesion"-"inicioSesion") as TimeSum FROM puzzlevid_session GROUP BY "usuarioId_id" ORDER BY TimeSum desc LIMIT 5;')
        tiempo_jugado = cursor.fetchall()
        print(tiempo_jugado)
        x = []
        for i in tiempo_jugado:
            x.append((i[0],i[1].total_seconds()/60))
        print(type(i[0][0]))
        data['tiempo_jugado']= x

        #Enemigos eliminados
        cursor.execute('SELECT "usuarioId_id", sum("enemigosEliminados") as EnemTotales FROM puzzlevid_session GROUP BY "usuarioId_id" ORDER BY EnemTotales desc LIMIT 5;')
        enemigos_eliminados = cursor.fetchall() 
        data["enemigos_eliminados"] = enemigos_eliminados

        # Duracion Promedio //Sin tabla
        cursor.execute('SELECT avg("terminoSesion"-"inicioSesion") as TimeAvg FROM puzzlevid_session ORDER BY TimeAvg desc;')
        duracion_promedio = cursor.fetchall()
        data['duracion_promedio']= duracion_promedio


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
    
    return render(request, 'estadisticasGlobales.html', {"data":data})

def signup(response):

    nombre=''
    apellido=''
    gametag=''
    #email=''
    #password=''
    #creadoEn= timezone.now()
    birth=''
    #id=2
    values_to_insert=[]
    

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            nombre= form.cleaned_data.get("nombre")
            apellido= form.cleaned_data.get("apellido")
            gametag= form.cleaned_data.get("username")
            birth= form.cleaned_data.get("nacimiento")
            form.save()
        values_to_insert = [nombre,apellido,gametag,birth]
        print(values_to_insert)
        #id=+1
        
        
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
    INSERT INTO puzzlevid_usuario (nombre,apellido,"gameTag",birth)
    VALUES (%s, %s, %s, %s)""", values_to_insert)
       
          


    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    
    finally:
        if(connection != None):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
            return redirect("/juega")
  
    
    
    return render(response, 'register/signup.html',{'form':form})


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

        nombre = request.user.username
        jugador_objeto = Usuario.objects.filter(gameTag=nombre)
        
        #print("user"+user)
        #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
        cursor = connection.cursor()
        #Display the PostgreSQL version installed
        cursor.execute('SELECT * from puzzlevid_session WHERE "usuarioId_id"={};'.format(jugador_objeto[0].id))
        rows = cursor.fetchall()
        
        #return HttpResponse(rows)
        data=[]
        data2=[]
        info={}
        
        for row in rows:
          retorno = {"usuarioId":jugador_objeto[0].id,
              "scoreQuimica":row[3],
              "scoreMate":row[4],
              "scoreGeografia":row[5],
              "scoreBiologia":row[9],
              "scoreHistoria":row[6],
              "EnemigosEliminados":row[7] 
            }
          data.append(retorno)
          
         
        print(data)

        for row in rows:
            retorno2 = {
                "usuarioId":row[8],
                "inicioSesion": row[1],
                "terminoSesion":row[2]
            }
            data2.append(retorno2)
       
          
        # Duracion Promedio //Sin tabla
        cursor.execute('SELECT avg("terminoSesion"-"inicioSesion") as TimeAvg FROM puzzlevid_session ORDER BY TimeAvg desc WHERE "usuarioId_id"={} ;'.format(jugador_objeto[0].id))
        duracion_promedio = cursor.fetchall()
        info['duracion_promedio']= str(duracion_promedio)

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

   
    return render(request, 'estadisticas.html', {"data":data,"data2":data2,"nombre":nombre,"info":info})
  
    
   

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
    jugador_objeto = Usuario.objects.filter(gameTag=jugador_o[0].username)
    print(jugador_o[0].password)
    #hash = computeMD5hash(jugador_o[0].password)
    if(len(jugador_o[0].password)>10):
        return HttpResponse(jugador_objeto[0].id)
    else:
        return HttpResponse(-1)

@csrf_exempt
def infoSession(request):
    body_unicode = request.body.decode('utf-8')
    print(body_unicode)
    body = loads(body_unicode)
    
    user = body['user_ID']
    inicioSesion = body ['inicio_sesion']
    terminoSesion = body ['termino_sesion']
    aciertosQuimica = body ['aciertosQuimica']
    aciertosMate = body['aciertosMate']
    aciertosGeo = body['aciertosGeo']
    aciertosHistoria = body['aciertosHistoria']
    aciertosBio = body ['aciertosBio']
    enemigosEliminados = body['enemigosEliminados']

    print(user + " " + inicioSesion + " " + terminoSesion + " " + aciertosQuimica + " " + aciertosMate + " " + aciertosGeo
    + " " + aciertosHistoria + " "+ aciertosBio + " " + enemigosEliminados)
    
    values_to_insert = [inicioSesion,terminoSesion,aciertosQuimica,aciertosMate,aciertosGeo,aciertosHistoria,enemigosEliminados,
                        user,aciertosBio]
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
    INSERT INTO puzzlevid_session ("inicioSesion","terminoSesion","aciertosQuim","aciertosMate","aciertosGeo","aciertosHist",
                                    "enemigosEliminados","usuarioId_id","aciertosBio")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", tuple(values_to_insert))

   

       
    #Handle the error throws by the command that is useful when using python while working with PostgreSQL
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    #Close the database connection
    
    finally:
        if(connection != None):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is now closed")
            return HttpResponse("200")



def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()
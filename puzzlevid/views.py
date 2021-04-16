from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from json import loads
import psycopg2
from puzzlevid.models import Usuario, Nivel, Session, Intento

# Create your views here.
def index(request):
    return render(request,'index.html')

def juega(request):
    return render(request, 'juega.html')

def steam(request):
    return render(request, 'steam.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

@csrf_exempt
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
    retorno={
        "userId":"diegoisunza@gmail.com",
        "valid":"True",
        "lastSession":"2021-03-21 19:04:02"
    }
    return JsonResponse(session)


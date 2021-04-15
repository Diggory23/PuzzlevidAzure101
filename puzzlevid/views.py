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

@csrf_exempt
def estadisticas(request):
    quimica =[]
    mate=[]
    geo=[]
    fisica=[]
    hist=[]
    enemigos=[]
    usuario_id=[]

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
        print(rows)
        return HttpResponse(rows)
         '''
        for row in rows:
           
            quimica.append(row[3])
            mate.append(row[4]
            geo= row[5]
            fisica =row[6]
            hist = row[7]
            enemigos = row[8]
            usuario_id = row[9]
           
        print(usuario_id)
         '''


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

    
    retorno = {"usuarioId":usuario_id,
              "scoreQuimica":quimica,
              "scoreMate":mate,
              "scoreGeografia":geo,
              "scoreFisica":fisica,
              "scoreHistoria":hist,
              "EnemigosEliminados":enemigos
        }
    print(retorno)
    return render(request, 'estadisticas.html', retorno)


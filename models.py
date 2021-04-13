from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.TextField()
    apellido = models.TextField()
    gameTag = models.TextField()
    email = models.TextField()
    password= models.TextField()
    creadoEn =models.DateTimeField()
    birth =models.DateField()


class Session(models.Model):
    usuarioId =  models.ForeignKey("Usuario", on_delete=models.SET_NULL, null=True)
    inicioSesion = models.DateTimeField()
    terminoSesion =models.DateTimeField()
    aciertosQuim = models.IntegerField()
    aciertosMate = models.IntegerField()
    aciertosGeo = models.IntegerField()
    aciertosFis = models.IntegerField()
    aciertosHist = models.IntegerField()
    enemigosEliminados = models.IntegerField()

class Nivel(models.Model):
    numeroNivel = models.IntegerField()
    nombreNivel = models.TextField()

class Intento(models.Model):
    nivelId =  models.ForeignKey("Nivel", on_delete=models.SET_NULL, null=True)
    sessionId =  models.ForeignKey("Session", on_delete=models.SET_NULL, null=True)
    numeroIntento = models.IntegerField()
    exito = models.NullBooleanField()
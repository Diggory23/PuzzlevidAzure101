from django.contrib import admin
from .models import Usuario, Session, Nivel, Intento

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Session)
admin.site.register(Nivel)
admin.site.register(Intento)

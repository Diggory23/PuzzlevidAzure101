from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name = 'index'),
    path('juega/',views.juega, name='juega'),
    path('steam/',views.steam, name='steam'),
    path('estadisticas',views.estadisticas, name='estadisticas')
]
from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.index, name = 'index'),
    path('juega',views.juega, name='juega'),
    path('signup',views.signup, name='signup'),
    path('estadisticas/',views.estadisticas, name='estadisticas'),
    path('login/',views.login, name ='login'),
    path('unity/', views.unity, name='unity'),
    path('infoUsuario/', views.infoUsuario, name='infoUsuario'),
    path('infoSession/', views.infoSession, name='infoSession'),
    path('estadisticasGlobales', views.estadisticasGlobales, name='estadisticasGlobales')
]
#unity pasa datos entre unity y la base de datos

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

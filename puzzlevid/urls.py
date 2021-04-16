from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name = 'index'),
    path('juega',views.juega, name='juega'),
    path('signup',views.signup, name='signup'),
    path('estadisticas',views.estadisticas, name='estadisticas'),
    path('login',views.login, name ='login'),
    path('unity/', views.unity, name='unity')
]

#unity pasa datos entre unity y la base de datos
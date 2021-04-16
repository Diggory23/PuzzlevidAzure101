from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name = 'index'),
    path('juega/',views.juega, name='juega'),
    path('signup/',views.signup, name='signup'),
    path('estadisticas/',views.estadisticas, name='estadisticas'),
    path('login/',views.login, name ='login'),
]
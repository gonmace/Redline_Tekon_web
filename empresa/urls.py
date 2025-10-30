from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [
    path('', views.home, name='home'),
    path('servicios/', views.servicios, name='servicios'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('clientes/', views.clientes, name='clientes'),
    path('equipo/', views.equipo, name='equipo'),
    path('contacto/', views.contacto, name='contacto'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
]



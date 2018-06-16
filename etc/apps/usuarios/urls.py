from django.urls import include
from django.urls import path
from apps.usuarios.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cotizacion',cotizar,name="cotizar"),
]



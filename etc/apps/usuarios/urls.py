from django.urls import include
from django.urls import path
from apps.usuarios.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cotizacion',cotizar,name="cotizar"),
    path('login', auth_views.login, {'template_name': 'registro/login.html'}, name='login'),
    path('registrarTraductor',TraductorSignUpView.as_view(),name='crear_traductor'),
    path('logout',LogoutView.as_view(), {'next_page':''},name='logout'),
    path('listar',cotizacion_list,name='listar'),
    path('descargar/<int:id_cotizacion>/',documento_descargar,name='documento_descargar'),
    path('responder/<int:id_cotizacion>/',responder_cliente,name='respuesta'),
    path('despachar/<int:id_cotizacion>/',despachar,name='despachar'),
    path('exito', RegistroView.as_view(),name='exito'),
]



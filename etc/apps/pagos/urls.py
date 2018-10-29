from django.urls import include
from django.urls import path
from apps.pagos.views import *
from django.urls import path, re_path
urlpatterns = [
    path('pago/<cotizacion_pk>/', PaypalView.as_view(),name="pago-paypal"),
    path('aceptar-pago/', PaypalExecuteView.as_view(),name="aceptar-pago-paypal"),
]
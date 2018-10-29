# Create your models here.
from django.db import models
from decimal import Decimal
from apps.usuarios.models import *

class PagoPaypalManager(models.Manager):
    def crear_pago(self, payment_id, cotizacion):
        pago=self.create(cotizacion=cotizacion,
            payment_id=payment_id,
            precio=cotizacion.precio,
            payer_email=cotizacion.email)
        return pago

class PagoPaypal(models.Model):
    # Foreign Key hacia la cotizacion de este pago
    cotizacion = models.ForeignKey(Cotizacion,on_delete=models.CASCADE)

    # Identificador de paypal para este pago
    payment_id = models.CharField(max_length=64, db_index=True)

    # Id unico asignado por paypal a cada usuario no cambia aunque
    # la dirección de email lo haga.
    payer_id = models.CharField(max_length=128, blank=True, db_index=True)

    # Dirección de email del cliente proporcionada por paypal.
    payer_email = models.EmailField(blank=True)

    # Guardamos una copia del precio de libro, porque puede variar en el tiempo
    precio = models.DecimalField(max_digits=8, decimal_places=2,
                default = Decimal('0.00'))

    pagado = models.BooleanField(default=False)

    objects = PagoPaypalManager()

    def __str__(self):
        return '{}'.format(self.cotizacion.titulo)

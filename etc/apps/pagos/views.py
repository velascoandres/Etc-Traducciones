# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from apps.usuarios.models import Cotizacion
from .models import PagoPaypal
from django.urls import reverse


import paypalrestsdk

# Create your views here.


class PaypalView(RedirectView):
    
    permanent = False

    def _generar_lista_items(self, cotizacion):
        """ """
        items = []
        items.append({
            "name":     "Traduccion: "+str(cotizacion),
            "sku":      str(cotizacion.id),
            "price":    ('%.2f' % cotizacion.precio),
            "currency": "USD",
            "quantity": 1,
        })
        return items


    def _generar_peticion_pago_paypal(self, cotizacion):
        """Crea el diccionario para genrar el pago paypal de libro"""
        peticion_pago = {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {                           
                "return_url": settings.SITE_URL+reverse('pagos:aceptar-pago-paypal'),
                "cancel_url": settings.SITE_URL},

            # Transaction - 
            "transactions": [ {
                # ItemList
                "item_list":{
                    "items": self._generar_lista_items(cotizacion)},

                # Amount
                "amount": {
                    "total": ('%.2f' % cotizacion.precio),
                    "currency": 'USD'},

                #Description
                "description": "Traduccion del documento: "+str(cotizacion),
                }]}

        return peticion_pago


    def _generar_pago_paypal(self, cotizacion):
        """Genera un pago de paypal para libro"""
        paypalrestsdk.configure({
            "mode":         settings.PAYPAL_MODE,
            "client_id":    settings.PAYPAL_CLIENT_ID,
            "client_secret":settings.PAYPAL_CLIENT_SECRET,})

        pago_paypal = paypalrestsdk.Payment(self._generar_peticion_pago_paypal(cotizacion))

        if pago_paypal.create():
            for link in pago_paypal.links:
                if link.method == "REDIRECT":
                    url_pago = link.href
        else:
            raise Exception(pago_paypal.error)

        return url_pago, pago_paypal


    def get_redirect_url(self, *args, **kwargs):
        """Extrae el libro que el usuario quiere comprar, genera un pago de 
        paypal por el precio del libro, y devuelve la direccion de pago que 
        paypal generó"""
        cotizacion = get_object_or_404(Cotizacion, pk=int(kwargs['cotizacion_pk']))
        url_pago, pago_paypal = self._generar_pago_paypal(cotizacion)

        # Se añade el identificador del pago a la sesion para que PaypalExecuteView 
        # pueda identificar al ususuario posteriorment
        self.request.session['payment_id'] = pago_paypal.id
        print ("Este es el PAGO")
        print (self.request.session['payment_id'])
        # Por ultimo salvar la informacion del pago para poder determinar que 
        # libro le corresponde, al terminar la transaccion.
        PagoPaypal.objects.crear_pago(pago_paypal.id, cotizacion)
 
        return url_pago



class PaypalExecuteView(TemplateView):
   
    template_name = 'pagos/exito.html'

    def _aceptar_pago_paypal(self, payment_id, payer_id):
        """Aceptar el pago del cliente, actualiza el registro con los datos
        del cliente proporcionados por paypal"""
        registro_pago = get_object_or_404(PagoPaypal, payment_id=payment_id)
        pago_paypal = paypalrestsdk.Payment.find(payment_id)
        print ("ESTE ES EL PAGO PAYPAL")
        print (pago_paypal)
        if pago_paypal.execute({'payer_id': payer_id}):
            registro_pago.pagado = True
            registro_pago.payer_id = payer_id
            registro_pago.payer_email = pago_paypal.payer['payer_info']['email']
            registro_pago.save()
        else:
            raise HttpResponseBadRequest

        return registro_pago
 
#Nias12345
    def get(self, request, *args, **kwargs):
    
        # Extraer identificacion de paypal del cliente, la id del pago,
        # y buscar el registro correspondiente.
        context = self.get_context_data(**kwargs)
        try:
            payer_id = request.GET['PayerID']
            print (request.session['payment_id'])
            payment_id = request.session['payment_id']
        except Exception:
            raise HttpResponseBadRequest

        registro_pago = self._aceptar_pago_paypal(payment_id, payer_id)
        
        return self.render_to_response(context)
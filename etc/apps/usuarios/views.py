
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

"""
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
"""
from django.views.generic import CreateView,TemplateView,ListView,FormView,RedirectView
from django.urls import reverse_lazy

#from apps.usuarios.models import *
from apps.usuarios.forms import *
from apps.usuarios.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


#from apps.usuarios.helpers import handle_uploaded_file, contadorPalabras, crearTXT, contarTXT
from apps.usuarios.helpers import *
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth import logout
from apps.pagos.models import *
import os
from django.conf import settings



class RegistroView(TemplateView):
    template_name = "cliente/info.html"

class TraductorSignUpView(CreateView):
    model = User
    form_class = TraductorSignUpForm
    template_name = 'registro/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Traductor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('usuarios:exito')

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def logout_us(request, *args, **kwargs):
    from django.utils import timezone
    user = request.user
    profile = user.get_profile()
    profile.last_logout = timezone.now()
    profile.save()
    logout(request, *args, **kwargs)

#Este metodo calculara el precio

def calcular_precio(idioma_or,idioma_dest,total):
    costo=Costo.objects.get(idioma_origen__nombre=idioma_or,idioma_destino__nombre=idioma_dest)
    print ("Este es el precio seleccionado")
    print (costo.precio_palabra)
    return costo.precio_palabra*total

def cotizar(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES)
        if form.is_valid():
            #cotizacion=form.save(calcular_precio())
            total=0
            if form.cleaned_data.get('texto'):
                txt=form.cleaned_data.get('texto')
                total=contarTXT(txt)
                crearTXT(txt,form.cleaned_data.get('titulo'))
            else:
                handle_uploaded_file(request.FILES['archivo'])
                total=contadorPalabras(request.FILES['archivo'].name)
            if total>0:
                cotizacion=form.save(calcular_precio(form.cleaned_data.get('idioma_origen'),form.cleaned_data.get('idioma_destino'),total))
                return render(request,'registro/respuesta.html',{'total':total,'cotizacion':cotizacion})
            else:
                form.error_archivo()
    else:
        form = CotizacionForm()
    return render(request, 'registro/cotizacion2.html', {'form': form})

#Lista las cotizaciones que se han comprado
def cotizacion_list(request):
    id_cotizaciones = PagoPaypal.objects.filter(pagado=True).values('cotizacion_id')
    print (id_cotizaciones)
    cotizaciones=Cotizacion.objects.filter(pk__in = id_cotizaciones,despachado=False)
    print (cotizaciones)

    contexto={'cotizaciones':cotizaciones}
    return render(request,'cliente/cotizacion_list.html',contexto)


#Vista para descargar el oa
def documento_descargar(request, id_cotizacion):
    
    try:
        path=Cotizacion.objects.get(id=id_cotizacion).file
        file_path = os.path.join(settings.MEDIA_ROOT, str(path))
    except:
        path=Cotizacion.objects.get(id=id_cotizacion).titulo
        file_path = os.path.join(settings.MEDIA_ROOT, str(path))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

#Vista que permite responder a un cliente determinado
def responder_cliente(request,id_cotizacion):
    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES)
        if form.is_valid():
                mensaje=form.cleaned_data.get('mensaje')
                email=Cotizacion.objects.get(id=id_cotizacion).email
                archivo=request.FILES['archivo']
                enviar_correo(email,archivo,mensaje)
                return redirect('usuarios:listar')

    else:
        form = RespuestaForm()
    return render(request, 'cliente/respuesta.html', {'form': form})

def enviar_correo(email,archivo,mensaje):
    from django.core.mail import EmailMessage
    msg = EmailMessage('Traduccion del documento', '{}'.format(mensaje), 'objetosaprendizajeslibres@gmail.com', ['{}'.format(email)])
    msg.content_subtype = "html"  
    msg.attach(archivo.name, archivo.read(), archivo.content_type)
    msg.send()
    return redirect('usuarios:listar')

#Vista que cambia el estado de una cotizacion
def despachar(request,id_cotizacion):
    Cotizacion.objects.filter(pk=id_cotizacion).update(despachado=True)
    return redirect('usuarios:listar')

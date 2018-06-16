
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



from apps.usuarios.helpers import handle_uploaded_file

def cotizar(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES)
        if form.is_valid():
        	print ("Se acepto")
        	handle_uploaded_file(request.FILES['file'],request.FILES['file'].name)
        	return HttpResponseRedirect('/')
    else:
        form = CotizacionForm()
    return render(request, 'registro/cotizacion.html', {'form': form})




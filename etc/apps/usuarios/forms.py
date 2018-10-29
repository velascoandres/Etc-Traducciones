from django import forms
from django.forms import widgets
from apps.usuarios.models import *
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.validators import FileExtensionValidator
from django.conf import settings

class TraductorSignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta(UserCreationForm.Meta):
		model = User
	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.email = self.cleaned_data["email"]
		user.is_traductor = True
		user.is_active = False
		user.save()
		return user


class RespuestaForm(forms.Form):
	mensaje=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Escribe el mensaje'}),label='Mensaje para el cliente',max_length=500,required=False)
	archivo=forms.FileField(label='Sube el archivo',required=False)


class CotizacionForm(forms.Form):
	titulo = forms.CharField(widget=forms.TextInput(attrs={'type':'string','placeholder':'Titulo'}),label='Titulo del documento',max_length=50)
	nombre = forms.CharField(widget=forms.TextInput(attrs={'type':'string','placeholder':'Nombre'}),label='Ingresa tu nombre',max_length=50)
	telefono = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono o Celular'}),label='Ingresa tu numero telefonico o celular',max_length=10)
	email =  forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Correo electronico'}),label='Ingresa tu correo electronico',max_length=30)
	fecha_limite=forms.DateField(label='Fecha limite de entrega',widget=forms.TextInput(attrs={'class':'datepicker'}))

	idioma_origen = forms.ModelChoiceField(
        queryset=Idioma.objects.all(),
        widget=forms.Select(),
        required=True,
        empty_label=None)

	idioma_destino = forms.ModelChoiceField(
        queryset=Idioma.objects.all(),
        widget=forms.Select(),
        required=True,
        empty_label=None)

	tipo_documento= forms.ModelChoiceField(
        queryset=Tipo_Documento.objects.all(),
        widget=forms.Select(),
        required=True,
        empty_label=None)
	archivo= forms.FileField(label='Sube el archivo',required=False,error_messages={'required': 'Sube un archivo docx !'})
	texto =  forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Pega el texto a traducir'}),label='Ingresa el texto a traducir',max_length=500,required=False)
	comentario= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Deja un comentario'}),label='Comentario o Instruccion',max_length=150,required=False)
	


	
	def save(self,precio):
		
		cotizacion = Cotizacion.objects.create(
			nombres=self.cleaned_data.get('nombre'),
			titulo=self.cleaned_data.get('titulo'),
			telefono=self.cleaned_data.get('telefono'),
			email=self.cleaned_data.get('email'),
			file=self.cleaned_data.get('archivo'),
			idioma_origen=self.cleaned_data.get('idioma_origen'),
			idioma_destino=self.cleaned_data.get('idioma_destino'),
			fecha_limite=self.cleaned_data.get('fecha_limite'),
			comentario=self.cleaned_data.get('comentario'),
			tipo_documento=self.cleaned_data.get('tipo_documento'),
			precio=precio)
		cotizacion.save()


		return cotizacion




	def clean(self):
		texto = self.cleaned_data.get('texto')
		archivo = self.cleaned_data.get('archivo')
		print (archivo)
		if not texto and not archivo:
			msg = forms.ValidationError("Se deben llenar los campos.")
			self.add_error('texto', msg)
		if texto and archivo:
			print ('archivo')
			msg = forms.ValidationError("Solo se debe pegar texto o subir un archivo.")
			self.add_error('texto', msg)
			self.add_error('archivo', msg)
		elif texto:
			self.cleaned_data['archivo'] = None
		elif archivo:
			import os
			ext = os.path.splitext(archivo.name)[1]  # [0] returns path+filename
			valid_extensions = ['.docx']
			if not ext.lower() in valid_extensions:
				raise forms.ValidationError('Ingrese un archivo del tipo \'.docx\' válido.')
			else:
				self.cleaned_data['texto'] = None


		return self.cleaned_data

	def error_archivo(self):
		msg=forms.ValidationError("Formato del archivo no compatible")
		self.add_error('archivo',msg)

from django import forms
from django.forms import widgets


class CotizacionForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'type':'string','placeholder':'Nombre'}),label='Ingresa tu nombre',max_length=50)
    numero = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono o Celular'}),label='Ingresa tu numero telefonico o celular',max_length=10)
    email =  forms.EmailField(widget=forms.TextInput(attrs={'Correo Electronico':'Nombre'}),label='Ingresa tu correo electronico',max_length=30)
    texto =  forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Pega el texto a traducir'}),label='Ingresa el texto a traducir',max_length=1000)
    archivo= forms.FileField(label='Sube el archivo',required=False)

        
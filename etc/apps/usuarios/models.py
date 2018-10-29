from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.



class User(AbstractUser):
    is_traductor = models.BooleanField(default=False)
    def __str__(self):
    	return '{}'.format(self.username)


class Idioma(models.Model):
	nombre=models.CharField(max_length=50)

	def __str__(self):
		return '{}'.format(self.nombre)

class Tipo_Documento(models.Model):
	nombre=models.CharField(max_length=50)
	def __str__(self):
		return '{}'.format(self.nombre)


class Cotizacion(models.Model):
	titulo=models.CharField(max_length=50)
	nombres=models.CharField(max_length=60)
	email = models.CharField(max_length=50)
	telefono = models.CharField(max_length=20)
	fecha_limite=models.DateField()
	file=models.FileField(upload_to="files",null=True, blank=True,default='vacio.zip')
	idioma_origen = models.ForeignKey(Idioma,null=False,blank=False,on_delete=models.CASCADE,related_name="idioma_origen")
	tipo_documento=models.ForeignKey(Tipo_Documento,null=False,blank=False,on_delete=models.CASCADE)
	idioma_destino = models.ForeignKey(Idioma,null=False,blank=False,on_delete=models.CASCADE,related_name="idioma_destino")
	comentario=models.CharField(max_length=300,null=True,blank=True,default='NO HAY COMENTARIO')
	precio=models.DecimalField(max_digits=6, decimal_places=2,null=False,blank=False,default = 0.00)
	despachado=models.BooleanField(default=False)

	def __str__(self):
		return '{}'.format(self.titulo)



class Costo(models.Model):
	idioma_origen=models.ForeignKey(Idioma,null=False,blank=False,on_delete=models.CASCADE,related_name="idioma_or")
	idioma_destino=models.ForeignKey(Idioma,null=False,blank=False,on_delete=models.CASCADE,related_name="idioma_dest")
	precio_palabra=models.DecimalField(max_digits=6, decimal_places=2,null=False,blank=False,default = 0.00)

	def __str__(self):
		return '{}-{}-{}'.format(self.precio_palabra,self.idioma_origen,self.idioma_destino)

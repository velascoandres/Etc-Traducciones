from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Idioma)
admin.site.register(Costo)
admin.site.register(Tipo_Documento)
admin.site.register(Cotizacion)
admin.site.register(User)

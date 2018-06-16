
from django.conf import settings


def handle_uploaded_file(f,nombre):
    with open(settings.MEDIA_ROOT+"/files/"+str(nombre),'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
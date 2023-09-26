from django.http import HttpResponse
from django.http import datetime

def timezone(request): #Zona horaria
    tiempo= "<h1>Tiempo: {0}</h1>".format(datetime.datetime.now())
    return HttpResponse(tiempo)

def home(request): #Primera vista
    1
    inicio = """ <html>
    <body>
    <h1>
    Smartings
    <h1>
    <body>
    <html>"""

    
    return HttpResponse(inicio)
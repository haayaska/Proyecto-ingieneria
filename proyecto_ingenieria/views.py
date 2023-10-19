from django.http import HttpResponse
import datetime
from django.template import Template, Context
import requests
from django.conf import settings
from django.http import JsonResponse
from .comunasCordenadas import buscarComuna, regionComunas



def home(request): #Primera vista
    1
    tiempo= "<h1>{0}</h1>".format(datetime.datetime.now().strftime("%A: %d/%m/%Y "))
    inicio = """ 
    <html>
    <body>
        <h1>The LECT Team is working on this web<h1>
        <h2> Cool things are comming soon...<h2>
    <body>
    <html>
    """
    texto = inicio + '\n' + tiempo
    return HttpResponse(texto)

def Presentacion(request):
    presentacionex = open("C:/Proyecto-ingieneria/Presentacion.htm") #el path no se detecta, podrian probar si funciona y avisar
    template= Template(presentacionex.read())                        #cuando lo vayan a probar cambien al path en donde se encuentra el archivo presentacion.html
    presentacionex.close()
    contexto = Context()
    docfinal = template.render(contexto)
    return HttpResponse(docfinal) #Habia un error, no se generaba una httpresponse 

def clima(request):
    data = buscarComuna(regionComunas)
    lat = data[1]
    lon = data[2]
    api_key = settings.OPENWEATHERKEY
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)


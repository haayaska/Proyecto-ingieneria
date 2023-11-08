from django.http import HttpResponse
import datetime
from django.template import Template, Context
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


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

'''def Presentacion(request):
    presentacionex = open('C:/Proyecto-ingieneria/plantillas/Presentacion.html') #el path no se detecta, podrian probar si funciona y avisar
    template= Template(presentacionex.read()) #cuando lo vayan a probar cambien al path en donde se encuentra el archivo presentacion.html
    presentacionex.close()
    contexto = Context()
    docfinal = template.render(contexto)
    return HttpResponse(docfinal) #Habia un error, no se generaba una httpresponse '''

def Presentacion(request):
    return render(request, 'main/Presentacion.html')

def clima(request):
    lat = '-33.0658'
    lon = '-71.3289' #cordenadas de villa alemana como prueba
    api_key = str(settings.OPENWEATHERKEY)
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    temperatura_kelvin = data.get('main', {}).get('temp') #esto sacara del json el valor de la temperatura en kelvin
    temperatura_celcius = round(temperatura_kelvin - 273.15) #transformara la temperatura de kelvin a celcius
    descripcion = data.get('weather', [])[0].get('description')
    tipos_climas = {"clear sky": ('Despejado', 0), # 0 significa "Apaga las luces"
                    "partly cloudy": ('Parcialmente Nublado', 1 ),
                    'overcast clouds': ('Nublado'),
                    "clouds": ('Nublado', 1 ),
                    "fog": ('Niebla', 1),
                    "mist": ('Neblina', 1 ),
                    "drizzle": ('Llovizna', 2), # 2 significa "Intenta apagar otros dispositivos para ahorrar energia"
                    "rain": ('Lluvioso', 2),
                    'moderate rain': ('Lluvia Moderada', 2),
                    "showers": ('Chubascos', 2),
                    "snow": ('Nieve', 3 ), # 3 Si utilizas dispositivos de calefaccion apaga las luces cuando sea necesario
                    "thunderstorm": ('Tormenta Electrica', 4),
                      }
    for llave in tipos_climas:
        if llave==descripcion:
            descripcion= tipos_climas[llave]
    ciudad = data.get('name')
    context = {
    'temperatura': temperatura_celcius,
    'descripcion': descripcion,
    'ciudad': ciudad
    }
    return render(request, 'clima.html', context)

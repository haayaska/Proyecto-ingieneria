from django.http import HttpResponse
import datetime
from django.template import Template, Context
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import time

def Presentacion(request):
    return render(request, 'main/Presentacion.html')

def consumo(request):

    return('hola')

def clima(request):
    lat = '-33.0333'
    lon = '-71.6667' 
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
            descripcion= (tipos_climas[llave])[0]
    ciudad = data.get('name')
    contextClima = {
    'temperatura': temperatura_celcius,
    'descripcion': descripcion,
    'ciudad': ciudad
    }
    return render(request, 'main/clima.html', contextClima)

def estadoLuz(request):
    deviceId = str(settings.DEVICE_ID)
    tk= 'Bearer ' + str(settings.SMART_THINGSTK)
    print(tk)
    url= f'https://api.smartthings.com/v1/devices/{deviceId}/components/main/capabilities/switch/status'
    response = requests.get(url, headers={"Authorization": tk})
    datos = response.json()
    contextAmpolleta= {"estado": datos.get('switch', {}).get('value')}
    return render(request, 'main/estados.html', contextAmpolleta)


def apagadoAuto(request):
    deviceId = str(settings.DEVICE_ID)
    tk= 'Bearer ' + str(settings.SMART_THINGSTK)
    body = {
    "commands": [
        {
        "component": "main",
        "capability": "switch",
        "command": "off",
        "arguments": []
        }
    ]
    }
    url= f'https://api.smartthings.com/v1/devices/{deviceId}/commands'
    response = requests.post(url,json=body, headers={"Authorization": tk})
    print(response.json())
    texto= 'aceptado'
    return(texto)

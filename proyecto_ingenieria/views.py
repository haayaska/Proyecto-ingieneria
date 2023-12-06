from django.http import HttpResponse
from django.template import Template, Context
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
import time
import datetime
import requests
from app.models import UserProfile

def presentacion(request):
    return render(request, 'main/Presentacion.html')

def registro(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            user = UserProfile.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                region=request.POST['region'],
                comuna=request.POST['comuna'],
                Smart_id=request.POST['smartid'],
                Smart_tkn=request.POST['smarttoken'],
                consumo=0
            )
            user.save()
            return render(request, 'registro.html')
        else:
            error_message = "Las contraseñas no coinciden."
            return render(request, 'registro.html', {'error': error_message})
    else:
        # Manejar el caso en el que el método HTTP es GET.
        return render(request, 'registro.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password) #
        print(user)

        if user is not None:
            print('entrando')
            login(request, user)
            return redirect('consumo')
        
        else:
            return render(request, 'main/login2.html', {
                    'error': 'Usuario o contraseña incorrecta'
                })
    else:
        return render(request, 'main/login2.html')

def consumo(request):
    #aqui esta la api de openweather:
    lat = '-33.0658'
    lon = '-71.3289' 
    api_key = str(settings.OPENWEATHERKEY)
    url1 = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url1)
    datas = response.json()
    temperatura_kelvin = datas.get('main', {}).get('temp') #esto sacara del json el valor de la temperatura en kelvin
    temperatura_celcius = round(temperatura_kelvin - 273.15) #transformara la temperatura de kelvin a celcius
    descripcion = datas.get('weather', [])[0].get('description') #sacara del json la descripcion del clima
    hora_actual = int((datetime.datetime.now()).hour)
    tipos_climas = {"clear sky": ('Despejado', 0),
                    "broken clouds": ('Nubes Dispersas', 0),
                    "few clouds": ('Unas Pocas Nubes', 0),
                    "scattered clouds": ('Nubes Dispersas', 0),
                    "partly cloudy": ('Parcialmente Nublado', 0 ),
                    'overcast clouds': ('Nublado', 1),
                    "clouds": ('Nublado', 1 ),
                    "fog": ('Niebla', 2),
                    "mist": ('Neblina', 2 ),
                    "drizzle": ('Llovizna', 3),
                    "light rain": ('Llovizna', 3), 
                    "rain": ('Lluvioso', 3),
                    'moderate rain': ('Lluvia Moderada', 3),
                    "heavy intensity rain":('Lluvia Fuerte', 3),
                    "very heavy rain":('Lluvia Fuerte', 3),
                    "extreme rain":('Lluvia Fuerte', 3),
                    "freezing rain": ('Lluvia Fuerte', 3),
                    "heavy intensity shower rain":('Lluvia Fuerte', 3),
                    "ragged shower rain":('Lluvia Fuerte', 3),
                    "shower rain":('Lluvia', 3),
                    "showers": ('Chubascos', 3),
                    "snow": ('Nieve', 4 ), 
                    "thunderstorm": ('Tormenta Electrica', 4),
                    
                      }
    for llave in tipos_climas:
        if llave==descripcion:
            descripcion= (tipos_climas[llave])[0]
            numero= (tipos_climas[llave])[1]
    ciudad = datas.get('name')
    #aqui esta la api de SMARTTHINGS:
    deviceId = str(settings.DEVICE_ID)
    tk= 'Bearer ' + str(settings.SMART_THINGSTK)
    url= f'https://api.smartthings.com/v1/devices/{deviceId}/components/main/capabilities/switch/status'
    response = requests.get(url, headers={"Authorization": tk})
    datos = response.json()
    estado= datos.get('switch', {}).get('value')
    if estado== 'off':
        estado= 'Apagado'
    else:
        estado= 'Encendido'
    if (numero== 0) and (estado == "Encendido") and (8<=hora_actual<21):
        off= 'off'
        apagadoAuto(request, off)
        estado = "Apagado"
    #diccionario context con todos los datos para la pagina de consumo
    context = {
    'temperatura': temperatura_celcius,
    'descripcion': descripcion,
    'ciudad': ciudad,
    'estado': estado,
    'numero':numero,
    }
    return render(request, 'main/consumo.html', context)

def estadoLuz(request):
    deviceId = str(settings.DEVICE_ID)
    tk= 'Bearer ' + str(settings.SMART_THINGSTK)
    url= f'https://api.smartthings.com/v1/devices/{deviceId}/components/main/capabilities/switch/status'
    response = requests.get(url, headers={"Authorization": tk})
    datos = response.json()
    contextAmpolleta= {"estado": datos.get('switch', {}).get('value')}
    return contextAmpolleta


def apagadoAuto(request, onOrOff):
    deviceId = str(settings.DEVICE_ID)
    tk= 'Bearer ' + str(settings.SMART_THINGSTK)
    body = {
    "commands": [
        {
        "component": "main",
        "capability": "switch",
        "command": onOrOff,
        "arguments": []
        }
    ]
    }
    url= f'https://api.smartthings.com/v1/devices/{deviceId}/commands'
    response = requests.post(url,json=body, headers={"Authorization": tk})
    return 


def contador(request, estadoLuz):
    usuario= UserProfile.objects.get(username="johna")
    print(usuario)
    contador= 0
    while estadoLuz == 'on':
        contado+=1
        print(contador)
        time.sleep(60)
    consumo= contador*15
    return(consumo)


#1 necesito que la funcion contador guarde en una base de datos el consumo conecetada a los usuarion como, nose
#2 Que la funcion corra en segundo plano
#3 que lo muestre en pantalla 

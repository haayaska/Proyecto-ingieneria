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
from app.models import *
from app.forms import EmailAuthenticationForm

def presentacion(request):
    return render(request, 'main/Presentacion.html')

def registro(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            try:
                user = UserProfile.objects.create_user(username=request.POST['username'],
                                                        email=request.POST['email'],
                                                        password=request.POST['password'],
                                                        region=request.POST['region'],
                                                        comuna=request.POST['comuna'],
                                                        Smart_id=request.POST['smartid'],
                                                        Smart_tkn=request.POST['smarttoken']
                                                        )
                user.save()
                login(request, user)
                return redirect('consumo')
            except IntegrityError:
                return render(request, 'main/registro.html', {
                    'error': 'El usuario ya existe'
                    })
        else:
            return render(request, 'main/registro.html', {
                'error': 'Las contraseñas no concuerdan.'
                })
    else:
        return render(request, 'main/registro.html')

def login(request):
    print(request.POST)
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('consumo')
            else:
                return render(request, 'main/login2.html', {
                    'error': 'Usuario o contraseña incorrecta'
                })
    else:
        return render(request, 'main/login2.html')

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
    '''if (numero== 0) and (estado == "on") and (8<=hora_actual<21):
        off= 'off'
        apagadoAuto(request, off)
        estado = "off"
    elif (numero!= 0) and (estado == "off"):
        on= 'on'
        apagadoAuto(request, on)
        estado= "on"'''
    #diccionario context con todos los datos para la pagina de consumo
    context = {
    'temperatura': temperatura_celcius,
    'descripcion': descripcion,
    'ciudad': ciudad,
    'estado': estado,
    'numero':numero
    }
    return render(request, 'main/consumo.html', context)

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



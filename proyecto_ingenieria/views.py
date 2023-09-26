from django.http import HttpResponse
import datetime
from django.template import Template, Context
def timezone(request): #Zona horaria
    tiempo= "<h1>Time: \n {0}</h1>".format(datetime.datetime.now().strftime("%A: %d/%m/%Y Hour:%H:%M"))
    return HttpResponse(tiempo)

def home(request): #Primera vista
    1
    inicio = """ 
    <html>
    <body>
    <h1>
    Smartings
    <h1>
    <body>
    <html>
    """
    return HttpResponse(inicio)

def test_plantilla(request):
    plantillaex = open('C:/Proyecto-ingieneria/Plantillas/plantilla1.html')
    template = Template(plantillaex.read())
    plantillaex.close()
    contexto = Context()
    documento = template.render(contexto)
    return HttpResponse(documento)

def plantilla_parametros(request):
    nombre= 'John Alvarado'
    plantillaex = open('C:/Proyecto-ingieneria/Plantillas/plantillaparametros.html')
    template = Template(plantillaex.read())
    plantillaex.close()
    contexto = Context({'nombreUsuario': nombre})
    documento = template.render(contexto)
    return HttpResponse(documento)
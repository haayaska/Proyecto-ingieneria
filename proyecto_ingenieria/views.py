from django.http import HttpResponse
import datetime
from django.template import Template, Context

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

def test_plantilla(request):
    plantillaex = open('C:/Proyecto-ingieneria/Plantillas/plantilla1.html')
    template = Template(plantillaex.read())
    plantillaex.close() 
    contexto = Context()
    documento = template.render(contexto)
    return HttpResponse(documento)

def Presentacion(request):
    presentacionex = open("plantillas\Presentacion.html")
    template= Template(presentacionex.read())
    presentacionex.close()
    contexto = Context()
    docfinal = template.render(contexto)
    return(docfinal)

from django.http import HttpResponse

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
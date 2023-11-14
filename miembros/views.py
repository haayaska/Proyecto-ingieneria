from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def inicioSesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('presentacion')
        else:
            messages.success(request, ('El usuario no exite'))
            return redirect('login')
    else:
        return render(request, 'templates/authenticate/login.html', {})



from django.urls import path
from . import views

urlpatterns = [
    path('inicioSesion', views.inicioSesion, name="login"),
]
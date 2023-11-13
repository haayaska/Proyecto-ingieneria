# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# establece la configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')

# crea una instancia de Celery y usa la configuración de Django
celery_app = Celery('tu_proyecto')

# carga las configuraciones de Celery desde tu archivo de configuración de Django
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# descubre automáticamente tareas en todas las aplicaciones de Django
celery_app.autodiscover_tasks()
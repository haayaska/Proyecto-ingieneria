from celery import shared_task
from views import estadoLuz
@shared_task
def tarea_compleja():
    
    return 'Tarea compleja finalizada'

from models import Model

# Realizar la consulta para obtener todos los objetos de TuModelo
resultados = Model.objects.all()

# Ahora 'resultados' contiene todos los objetos de la tabla TuModelo
# Puedes iterar sobre ellos para acceder a los valores de las columnas
for objeto in resultados:
    valor_columna1 = objeto.columna1
    valor_columna2 = objeto.columna2
    # ...

# O si solo quieres los valores de una columna específica
usuario = Model.objects.values_list('username', flat=True)
email = Model.objects.values_list('email', flat=True)
password = Model.objects.values_list('password', flat=True)
region = Model.objects.values_list('region', flat=True)
comuna = Model.objects.values_list('comuna', flat=True)
sID = Model.objects.values_list('Smart_id', flat=True)
tkn = Model.objects.values_list('Smart_tkn', flat=True)
print( usuario, email, password,region,comuna,sID, tkn)



# Ahora 'valores_columna1' contiene todos los valores de la columna1
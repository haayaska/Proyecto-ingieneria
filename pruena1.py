from random import randint
x= randint(1,100)
flag= True
flag2= True
counter= 0
while flag2:
    intentos= int(input('Ingresa cuantos intentos chimbones vas a tener entre 1 y 100: '))
    if (intentos>0) and (101>intentos):
        flag2= False
    else:
        print('Esa no es una opcion disponible sapo hijueputa')
while flag:
    counter+=1
    y= int(input('Ingresa Tu Numerito Mondaa: '))
    if counter == intentos:
        print('No te alcanzo care chimbaa')
        flag= False
    if (y!= x) and (counter!=intentos):
        print('Ese no es CareMondaa')
    if (y== x) and (counter!=intentos):
        print('Adivinaste SapoHijueputa el numero era: ', x, ' te demoraste: ', counter, ' de ', intentos, ' intentos ')
        flag= False
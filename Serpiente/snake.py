#Agente inteligente
#Serpiente

import pygame, sys
from pygame.locals import *
from random import randrange

#Variables para reloj
delay_clock = pygame.time.Clock()
sleep = 30

#Colores para la serpiente, suelo y comida
color_serpiente = (200, 200, 200)
color_suelo = (10, 10, 10)
color_comida = (30, 25, 70)
color_muro = (225, 225, 225)

#Definicion de dimensiones del mapa, junto con sus muros presentes
dimension = 20
celdas_x = 20
celdas_y = 20

ancho = celdas_x * dimension
alto = celdas_y * dimension

#Comida encontrada
#0, inicialmente
comida_encontrada = 0

mapa = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#Se debe tener en cuenta que los muros van a estar representados por un 1,
#la comida por un 2, y la serpiente puede andar por encima de si
muro = 1
comida = 2

#Cambiar la poscicion de la comida
#Se cuida que no este sobre un muro
pos_comida = [randrange(celdas_y), randrange(celdas_x)]
while(mapa[pos_comida[0]][pos_comida[1]] == muro):
	pos_comida = [randrange(celdas_y), randrange(celdas_x)]
mapa[pos_comida[0]][pos_comida[1]] = comida

print(mapa)


#------------- Modelo de la serpiente ---------------------------------------
#posicion inicial de la serpiente al iniciar la secuencia de movimiento
pos_serpiente = [[1, 1], [1, 2], [1, 3], [1, 4]]

'''
El movimiento de la serpiente se puede modelar en una maquina de estados.
Las transiciones dependen de la direccion actual, de la posicion de la 
cabeza de la serpiente y de el ciclo en el que se encuentra.
El ciclo es la referencia que utiliza la serpiente para determinar si
se dirige hacia abajo o hacia arriba en el recorrido de cascada.El ciclo
puede ser 1 para arriba y 0 para abajo. Inicialmente es 0.
La direccion de la serpiente se representa con 4 numeros. Puede ser:
1- derecha
2- izquierda
3- abajo
4- arriba
'''

ciclo = 0

#La direccion inicial de la serpiente es hacia la derecha
direccion = 1

def desplazar(direccion):
    #Desplazar un cuadro a la derecha
    if direccion == 1:
        pos_serpiente[0] = pos_serpiente[1]
        pos_serpiente[1] = pos_serpiente[2]
        pos_serpiente[2] = pos_serpiente[3]
        pos_serpiente[3] = [pos_serpiente[3][0], pos_serpiente[3][1] + 1]
    elif direccion == 2:
        pos_serpiente[0] = pos_serpiente[1]
        pos_serpiente[1] = pos_serpiente[2]
        pos_serpiente[2] = pos_serpiente[3]
        pos_serpiente[3] = [pos_serpiente[3][0], pos_serpiente[3][1] - 1]
    elif direccion == 3:
        pos_serpiente[0] = pos_serpiente[1]
        pos_serpiente[1] = pos_serpiente[2]
        pos_serpiente[2] = pos_serpiente[3]
        pos_serpiente[3] = [pos_serpiente[3][0] + 1, pos_serpiente[3][1]]
    elif direccion == 4:
        pos_serpiente[0] = pos_serpiente[1]
        pos_serpiente[1] = pos_serpiente[2]
        pos_serpiente[2] = pos_serpiente[3]
        pos_serpiente[3] = [pos_serpiente[3][0] - 1, pos_serpiente[3][1]]

def moverSerpiente(cabeza, ciclo, direccion):
    #Se revisa si hay que cambiar el ciclo basado en la posicion de la serpiente
    #Si esta en el fondo debe subir, y si está arriba tiene que bajar
    if ciclo == 0 and cabeza[0] == 18:
        ciclo = 1
    if ciclo == 1 and cabeza[0] == 1:
        ciclo = 0
    #Cambiar la direccion de la serpiente segun la posicion, ciclo y direccion

    #Si va a la derecha, pregunta si hay muro en frente suyo. Si lo hay, y el ciclo
    #es de descenso, entonces baja la cabeza y se desplaza. Si no hay muro, entonces
    #continua hacia la derecha
    if direccion == 1 and mapa[cabeza[0]][cabeza[1]+1] == muro and ciclo == 0:
        direccion = 3
    elif direccion == 3 and mapa[cabeza[0]][cabeza[1]+1] == muro and ciclo == 0:
        direccion = 2
    elif direccion == 2 and mapa[cabeza[0]][cabeza[1]-1] == muro and ciclo == 0:
        direccion = 3
    elif direccion == 3 and mapa[cabeza[0]][cabeza[1]-1] == muro and ciclo == 0:
        direccion = 1

    elif direccion == 1 and mapa[cabeza[0]][cabeza[1]+1] == muro and ciclo == 1:
        direccion = 4
    elif direccion == 4 and mapa[cabeza[0]][cabeza[1]+1] == muro and ciclo == 1:
        direccion = 2
    elif direccion == 2 and mapa[cabeza[0]][cabeza[1]-1] == muro and ciclo == 1:
        direccion = 4
    elif direccion == 4 and mapa[cabeza[0]][cabeza[1]-1] == muro and ciclo == 0:
        direccion = 1
    elif direccion == 3 and mapa[cabeza[0]][cabeza[1]+1] == muro and ciclo == 1:
        direccion = 2

    #Se desplaza la serpiente
    desplazar(direccion)
    '''
    print('-----------------------------------')
    print(mapa[cabeza[0]][cabeza[1]+1])
    print(direccion)
    print(cabeza)
    print(ciclo)
    '''
    return [ciclo, direccion]


#Realiza o no una accion si encuentra o no comida
def askComida(adrs_snake):
    if mapa[adrs_snake[len(adrs_snake) - 1][0]][adrs_snake[len(adrs_snake) - 1][1]] == comida:
        mapa[adrs_snake[len(adrs_snake) - 1][0]][adrs_snake[len(adrs_snake) - 1][1]] = 0
        #comida_encontrada = comida_encontrada + 1
        #Es necesario cambiar la posicion de la comida cada vez que sea encontrada
        pos_comida = [randrange(celdas_y), randrange(celdas_x)]
        while(mapa[pos_comida[0]][pos_comida[1]] == muro):
            pos_comida == [randrange(celdas_y), randrange(celdas_x)]
        mapa[pos_comida[0]][pos_comida[1]] == 2
    print(comida_encontrada)
    params = moverSerpiente(pos_serpiente[3], ciclo, direccion)
    return params
    #Despues de que se revisa si hay comida, se pasa a modelar el siguiente movimiento
    #moverSerpiente()

#------------- Fin - Modelo de la serpiente ---------------------------------

#----------------------------------------------------------------------------

#Funcion para dibujar un rectangulo relleno
def dibujarCuadro(color, dimension_cuadro): #Recibe el color y las dimensiones como parametro
    pygame.draw.rect(ventana, color, pygame.Rect(dimension_cuadro), 0)

#Funcion para dibujar el mapa con sus correspondientes colores
#de comida, suelo y muros
'''def dibujarMapa():
	for fila in range(len(mapa)):
		for columna in range(len(mapa)):
			if mapa[fila][columna] == comida:
				dibujarCuadro(color_comida, ((dimension*fila), (dimension*columna), dimension, dimension))
			elif mapa[fila][columna] == muro:
				dibujarCuadro(color_muro, ((dimension*fila), (dimension*columna), dimension, dimension))
'''

def dibujarSerpiente(adrs_snake):
	for adrs in adrs_snake:
		dibujarCuadro(color_serpiente, ((dimension*adrs[1]), (dimension*adrs[0]), dimension, dimension))

#Confusion espacial (?
def dibujarMapa():
	for fila in range(len(mapa)):
		for columna in range(len(mapa)):
			if mapa[fila][columna] == comida:
				dibujarCuadro(color_comida, ((dimension*columna), (dimension*fila), dimension, dimension))
			elif mapa[fila][columna] == muro:
				dibujarCuadro(color_muro, ((dimension*columna), (dimension*fila), dimension, dimension))
#----------------------------------------------------------------------------

#Inicializar ventana
pygame.init()
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Snakeft')

#Mostrar pantalla
while True:
    #Mostrar el mapa y rellenar el suelo y la serpiente
    ventana.fill(color_suelo)
    dibujarMapa()
    dibujarSerpiente(pos_serpiente)
    params = askComida(pos_serpiente)
    ciclo = params[0]
    direccion = params[1]

    #La serpiente comienza a realizar movimientos

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    #Timing para el movimiento/actualizacion de la pantalla
    delay_clock.tick(sleep)
    #Actualizar pantalla
    pygame.display.update()

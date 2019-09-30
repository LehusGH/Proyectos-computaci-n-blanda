#Agente inteligente
#Serpiente

import pygame, sys
from pygame.locals import *
from random import randrange

#Variables para reloj
delay_clock = pygame.time.Clock()
sleep = 20

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
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
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
while(mapa[pos_comida[0]][pos_comida[1]] == 1):
	pos_comida = [randrange(celdas_y), randrange(celdas_x)]
mapa[pos_comida[0]][pos_comida[1]] = comida

print mapa


#------------- Modelo de la serpiente ---------------------------------------

#Realiza o no una accion si encuentra o no comida
def askComida(adrs_snake):
	if mapa[adrs_snake[len(adrs_snake) - 1][0]][adrs_snake[len(adrs_snake) - 1][1]] == comida:
		comida_encontrada += 1
		#Es necesario cambiar la posicion de la comida cada vez que sea encontrada
		pos_comida = [randrange(celdas_y), randrange(celdas_x)]
	while(mapa[pos_comida[0]][pos_comida[1]] == 1):
		pos_comida = [randrange(celdas_y), randrange(celdas_x)]
	mapa[pos_comida[0]][pos_comida[1]] = comida

	else:
		print 'No hay nada'

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
3- arriba
4- abajo
'''

ciclo = 0

def moverSerpiente(direccion_actual, cabeza):
	pass

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
	askComida(pos_serpiente)

	#La serpiente comienza a realizar movimientos

	for evento in pygame.event.get():
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()

	#Timing para el movimiento/actualizacion de la pantalla
	delay_clock.tick(sleep)
	#Actualizar pantalla
	pygame.display.update()
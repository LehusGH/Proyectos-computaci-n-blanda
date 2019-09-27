import pygame, sys
from pygame.locals import*
from random import randrange

#Realizado por Leandro Hurtado Salazar
#Codigo: 1004775466


#Variables de reloj -> para que la serpiente no se mueva tan rapido
fps_clock = pygame.time.Clock()
sleep = 15
#Color de la serpiente
color_serpiente = (200, 200, 200)
#Color del fondo
color_suelo = (5, 5, 5)
#Color de la comida
color_comida = (110, 90, 55)
#Color de los muros
color_ladrillo = (160, 40, 30)

#Cuerpo de la serpiente
#La primera lista de la serpiente sera la cola
#La ultima lista de la serpiente sera la cabeza
serpiente = [[20, 20], [40, 20], [60, 20], [80, 20]]
direccion = 6

#Posicion inicial de la comida 
comida = [(randrange(18)*20), (randrange(32)*20)]
while((comida[0] == 0) or (comida[0] == 31) or (comida[1] == 0) or (comida[1] == 31)):
    comida = [(randrange(18)*20), (randrange(32)*20)]

#Crear la matriz que representará los objetos que hay presentes en el mapa
lineas_x = 18
lineas_y = 32
matriz_mapa = []
for i in range(lineas_x):
    matriz_mapa.append([0]*lineas_y)

#Llenar los bordes del mapa con 1 como identificador
for i in range(32):
    matriz_mapa[0][i] = 1
for i in range(32):
    matriz_mapa[17][i] = 1
for i in range(18):
    matriz_mapa[i][0] = 1
for i in range(18):
    matriz_mapa[i][31] = 1

matriz_mapa[int(comida[0]/20)][int(comida[1]/20)] = 2
print(matriz_mapa)
#Mover la serpiente hacia la derecha
def derecha(cuerpo):
    for i in range(len(cuerpo)-1):
        cuerpo[i][0] = cuerpo[i+1][0]
        cuerpo[i][1] = cuerpo[i+1][1]
    cuerpo[len(cuerpo)-1][0] += 20
    return cuerpo

#Mover la serpiente hacia abajo
def abajo(cuerpo):
    for i in range(len(cuerpo)-1):
        cuerpo[i][0] = cuerpo[i+1][0]
        cuerpo[i][1] = cuerpo[i+1][1]
    cuerpo[len(cuerpo)-1][1] += 20
    return cuerpo

#Mover la serpiente hacia la izquierda
def izquierda(cuerpo):
    for i in range(len(cuerpo)-1):
        cuerpo[i][0] = cuerpo[i+1][0]
        cuerpo[i][1] = cuerpo[i+1][1]
    cuerpo[len(cuerpo)-1][0] -= 20
    return cuerpo

#Mover la serpiente hacia arriba
def arriba(cuerpo):
    for i in range(len(cuerpo)-1):
        cuerpo[i][0] = cuerpo[i+1][0]
        cuerpo[i][1] = cuerpo[i+1][1]
    cuerpo[len(cuerpo)-1][1] -= 20
    return cuerpo

#Funcion para dibujar un rectangulo relleno
def dibujar_cuadro(color, dimension_cuadro): #Recibe el color y las dimensiones como parametro
    pygame.draw.rect(ventana, color, pygame.Rect(dimension_cuadro), 0)

#Funcion para dibujar la serpiente completa
def dibujar_serpiente(cuerpo):
    for i in range(len(cuerpo)):
        dimension_cuerpo = (cuerpo[i][0], cuerpo[i][1], 20, 20)
        dibujar_cuadro(color_serpiente, dimension_cuerpo)

#Inicializar ventana
pygame.init()
ventana = pygame.display.set_mode((360, 640))
pygame.display.set_caption("Snake IA")

#Poner la venta a mostrarse
while True:
    ventana.fill(color_suelo)
    #dibujar_cuadro(color_comida, (comida[0], comida[1], 20, 20))

    #Dibujar los bordes del mapa
    for i in range(18):
        for j in range(32):
            if(matriz_mapa[i][j] == 1):
                dibujar_cuadro(color_ladrillo, (i*20, j*20, 20, 20))

    #Ir arriba equivale a 8
    #Ir abajo equivale a 2
    #Ir a la derecha equivale a 6
    #Ir a la izquierda equivale a 4
    if(direccion == 6):
        serpiente = derecha(serpiente)
        dibujar_serpiente(serpiente)
    elif(direccion == 2):
        serpiente = abajo(serpiente)
        dibujar_serpiente(serpiente)
    elif(direccion == 8):
        serpiente = arriba(serpiente)
        dibujar_serpiente(serpiente)
    elif(direccion == 4):
        serpiente = izquierda(serpiente)
        dibujar_serpiente(serpiente)

    dibujar_cuadro(color_comida, (comida[0], comida[1], 20, 20))
    #Cambiar la direccion de la serpiente dependiendo de su posicion en el mapa
    pos_cabeza = [serpiente[(len(serpiente)-1)][0]/20, serpiente[(len(serpiente)-1)][1]/20]

    if(matriz_mapa[int(pos_cabeza[0]+1)][int(pos_cabeza[1])] == 2):
        if direccion == 6:
            serpiente.append([serpiente[(len(serpiente)-1)][0]+20, serpiente[(len(serpiente)-1)][1]])
        elif direccion == 4:
            serpiente.append([serpiente[(len(serpiente)-1)][0]-20, serpiente[(len(serpiente)-1)][1]])

    #Girar la serpiente hacia la izquierda luego de haber bajado
    if (direccion == 2) and (matriz_mapa[int(pos_cabeza[0]+1)][int(pos_cabeza[1])] == 1):
        print("cambio de direccion")
        direccion = 4
    
    #Girar la serpiente a la derecha luego de haber bajado
    if (direccion == 2) and (matriz_mapa[int(pos_cabeza[0]-1)][int(pos_cabeza[1])] == 1):
        print("cambio de direccion")
        direccion = 6

    #Girar la serpiente hacia abajo en caso de estar ubicada al extremo derecho
    if (direccion == 6) and (matriz_mapa[int(pos_cabeza[0]+1)][int(pos_cabeza[1])] == 1):
        print("Vas a chocar!")
        direccion = 2

    #Girar la serpiente hacia abajo en caso de estar ubicada al extremo derecho
    if (direccion == 4) and (matriz_mapa[int(pos_cabeza[0]-1)][int(pos_cabeza[1])] == 1):
        print("Vas a chocar!")
        direccion = 2

        


    #Lectura de eventos... inservible de momento
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
    #Timing del movimiento de la serpiente
    fps_clock.tick(sleep)

    #Actualizar la ventana
    pygame.display.update()
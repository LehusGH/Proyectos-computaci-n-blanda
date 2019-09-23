#Libreria de manejo de graficos para python
import pygame

#Ancho y alto de la pantalla
w = 500
h = 500

#Esta funcion se encarga de cargar las imagenes de las autopistas
#Retorna la imagen de fondo de autopista
def load_image(filename):
    image = pygame.image.load(filename)
    return image

#Función para mostrar todos los elementos graficos en la ventana
def print_window():
    #Inicializar pygame
    #Titulo de ventana
    #tamaño de ventana
    pygame.init()
    pygame.display.set_caption("simulación auto-motor")
    window = pygame.display.set_mode((w, h))

    #Prueba dibujo de cuadrado
    #draw_square(window, color_asphalt, 50, 50, 20, 20)
    #Insertar todos los procesos necesarios en el siguiente bloque
    #-------------------------------------------------------------
    bg_asphalt = load_image('Imagenes/pista1.jpg')
    window.blit(bg_asphalt, (0,0))
    #-------------------------------------------------------------

    #Refrescar la pantalla
    pygame.display.flip()

    #Lectura de eventos
    #Cerrar los procesos
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
    
    #Mostrar la imagen de fondo en pantalla

    #Finalizar todos los procesos
    pygame.quit()

if __name__ == '__main__':
    print_window()
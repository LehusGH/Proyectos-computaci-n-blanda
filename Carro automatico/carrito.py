# -*- coding: utf-8 -*-
# Libreria de manejo de graficos para python
import pygame

# Ancho y alto de la pantalla
w = 1000
h = 1000

NEGRO = (0,0,0)
ROJO = (255,0,0)
AZUL = (0,0,255)
BLANCO = (255,255,255)

# Esta funcion se encarga de cargar las imagenes de las autopistas
# Retorna la imagen de fondo de autopista
def load_image(filename):
	image = pygame.image.load(filename).convert_alpha()
	return image

# Recortar imagen
# Para sabanas de sprites
# x = cantidad de columnas, y = cantidad de filas, z = ancho en pixeles de cada segmento, 
# w = alto en pixeles de cada segmento
def recortar(archivo,x=1,y=1,z=32,w=32):
	fondo=pygame.image.load(archivo).convert_alpha()
	info=fondo.get_size()
	info_ancho=info[0]
	info_alto=info[1]
	cx=info_ancho/x
	cy=info_alto/y
	m=[]
	for i in range(x):
		la=[]
		for j in range(y):
			cuadro =[z*i,j*w,cx,cy]
			recorte=fondo.subsurface(cuadro)
			la.append(recorte)
		m.append(la)
	return m

# Carrito

class carrito(pygame.sprite.Sprite):
	def __init__(self, img_sprite,x,y):
		pygame.sprite.Sprite.__init__(self)
		# Se le carga una imagen al objeto, sea por load_image o por recortar
		self.m=img_sprite
		self.image=self.m[0][0]
		self.rect= self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direccion = 'U'
		self.velocidad = 10
		# El radio usado para las colisiones que simularán los sensores
		self.radius = 120

	def update(self):
		if self.rect.y <= 0:
			self.rect.y = 1000 - self.rect.height
		self.rect.y-=self.velocidad

# Semaforo
# se crea con semaforo_color_uva_maracuya(<nombre de la imagen recortada>, <posición en x>,
# <posición en y>)
class semaforo_color_uva_maracuya(pygame.sprite.Sprite):
	
	def __init__(self, img_sprite,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.m=img_sprite
		self.image=self.m[0][0]
		self.rect= self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.estado = 1
		self.estado_previo = 1
		self.tiempo_de_cambio = 100

	# Cambia color dependiendo del estado cada tanto tiempo
	def update(self):
		# Cambia
		if self.tiempo_de_cambio == 0:
			# si esta en Rojo
			if self.estado == 1:
				self.estado = 2
				self.estado_previo = 1
				self.tiempo_de_cambio = 50
			# si esta en Amarillo
			elif self.estado == 2:
				# y antes estuvo en Rojo
				if self.estado_previo == 1:
					self.estado = 3
				# y antes estuvo en Verde
				else:
					self.estado = 1
				self.tiempo_de_cambio = 200
			# si está en verde
			else:
				self.estado = 2
				self.estado_previo = 3
				self.tiempo_de_cambio = 50
		# No cambia
		else:
			self.tiempo_de_cambio -= 1
		self.image=self.m[0][self.estado-1]

# Se mira que el carro esté en dirección hacia el semáforo
# se retorna 0 para detener el carro y 1 para avanzar
def percepciones(car, soum):
	'''or ((car.direccion == 'D') and (car.rect.y < soum.rect.y)) or ((car.direccion == 'L') and 
	(car.rect.x < soum.rect.x)) or ((car.direccion == 'R') and (car.rect.x > soum.rect.x))'''
	if ((car.direccion == 'U') and (car.rect.y > soum.rect.y)) :
		if soum.estado == 1:
				return 0
		elif soum.estado == 2:
			if soum.estado_previo == 1:
				return 1
			else:
				return 0
		else:
			return 1

# Dependiendo de la percepción permite continuar al carro o hace que se detenga
def acciones(percepcion, car):
	if percepcion == 0:
		# si no está detenido
		if car.velocidad >= 0:
			car.velocidad = 0
	else:
		# si no está avanzando
		if car.velocidad <= 10:
			car.velocidad = 10

# Funcion para mostrar todos los elementos graficos en la ventana
def print_window():
	#Inicializar pygame
	#Titulo de ventana
	#tamanhio de ventana
	pygame.init()
	pygame.display.set_caption("simulacion auto-motor")
	window = pygame.display.set_mode((w, h))

	# Prueba dibujo de cuadrado
	# draw_square(window, color_asphalt, 50, 50, 20, 20)
	# Insertar todos los procesos necesarios en el siguiente bloque

	#-------------------------------------------------------------

	# Pantalla de de pista 1
	bg_asphalt = load_image('pista1.png')
	window.blit(bg_asphalt, (0,0))

	# Se crea el semaforo
	soumagen = recortar('semaforo.png',1,3,32,64)
	soum = semaforo_color_uva_maracuya(soumagen,668,434)

	# Grupo de semaforos
	semaforos = pygame.sprite.Group()
	semaforos.add(soum)

	# Se crea el carro
	carrimagen = recortar('carro.png',1,1,64,120)
	carrote = carrito(carrimagen,600,820)
	# Grupo de carros
	carros = pygame.sprite.Group()
	carros.add(carrote)

	#-------------------------------------------------------------


	# Refrescar la pantalla
	pygame.display.flip()

	# Reloj
	reloj=pygame.time.Clock()

	# Fin de ejecución
	fin = False

	# Lectura de eventos
	# Cerrar los procesos

	while not fin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				fin = True

		# Detección de cercanía a un semáforo
		# pygame.sprite.collide_circle usa un radio definido para el objeto, el radio es opcional, si no hay un 
		# radio definido esto toma uno que sea capaz de encerrar los objetos
		# para este caso 'carrote' tiene radio definido en la clase 'carrito', pero los semaforos no
		# ------------------------------------------------------------------------------------------------------
		# En caso de usar más carros:
		# for coche in carros:
		# semaforo_detector = pygame.sprite.spritecollide(coche, semaforos, False, pygame.sprite.collide_circle)
		# for detectado in semaforo_detector:
		#	acciones(percepciones(coche,detectado),coche)
		# ------------------------------------------------------------------------------------------------------

		semaforo_detector = pygame.sprite.spritecollide(carrote, semaforos, False, pygame.sprite.collide_circle)
		for detectado in semaforo_detector:
			# Aquí se ejecuta la función del agente inteligente
			acciones(percepciones(carrote,detectado),carrote)

		# Refresco de pantalla
		window.blit(bg_asphalt, (0,0))
		semaforos.update()
		semaforos.draw(window)
		carros.update()
		carros.draw(window)

		pygame.display.flip()
		reloj.tick(60)

	
	# Mostrar la imagen de fondo en pantalla

	# Finalizar todos los procesos
	pygame.quit()
	

if __name__ == '__main__':
	print_window()
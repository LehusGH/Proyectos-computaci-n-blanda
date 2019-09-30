import sys
import os
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K

K.clear_session()

data_entrenamiento = 'Data/Entrenamiento'
data_validacion = 'Data/Validacion'
direccion = 'Modelo/'

#------------------- PARAMETROS -----------------------
#Numero de iteaciones sobre el dataset construido
epocas = 20
#Tamaño para procesar las imagenes a la red neuronal
altura, longitud = 100, 100
#Numero de imagenes a mandar a la computadora
batch_size = 32
#Numero de veces a procesar la información de los datasets por epoca
pasos = 1000
#Numero de pasos de validacion por epoca
pasos_validacion = 200
#Numero de filtros a aplicar a cada convolucion
filtros_conv1 = 32
filtros_conv2 = 64
tam_filtro1 = (3, 3)
tam_filtro2 = (2, 2)
#Tamaño de filtro en el MAX Pooling
tam_pool = (2, 2)
#Numero de clases
clases = 3
#Factor de aprendizaje Learning Rate
lr = 0.0005
#------------------------------------------------------

#Preprocesamineto de imagenes
#------------------------------------------------------
entrenamiento_datagen = ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.3,
    zoom_range = 0.3,
    horizontal_flip = True
)

validacion_datagen = ImageDataGenerator(
    rescale = 1./255
)

imagen_entrenamiento = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,
    target_size = (altura, longitud),
    batch_size = batch_size,
    class_mode = 'categorical'  #Es una clasificacion categorica para amarillo, verde y rojo
)

imagen_validacion = validacion_datagen.flow_from_directory(
    data_validacion,
    target_size = (altura, longitud),
    batch_size = batch_size,
    class_mode = 'categorical'
)
#------------------------------------------------------

#Red neuronal para clasificar imagenes CNN
#------------------------------------------------------
cnn = Sequential()  #Es una composicion de capas

#Capa 1 de convolucion
cnn.add(Convolution2D(filtros_conv1, tam_filtro1, padding = 'same', input_shape = (altura, longitud, 3), activation = 'relu'))

#Capa 1 de pooling
cnn.add(MaxPooling2D(pool_size = tam_pool))

#Capa 2 de convolucion
cnn.add(Convolution2D(filtros_conv2, tam_filtro2, padding = "same", activation = 'relu'))

#Capa 1 de pooling
cnn.add(MaxPooling2D(pool_size = tam_pool))

#Convertir la imagen de 2 dimensiones en un solo vector
#o lista que contiene toda la informacion de la imagen
cnn.add(Flatten())

#La red neuronal consta de 256 neuronas por capa
cnn.add(Dense(256, activation = 'relu'))

#A la capa densa se le apaga el 50% de las neuronas
#Esto se hace para que no se cree un unico camino donde solo
#se reconozca un tipo de semaforo
#Es mas adaptable a informacion nueva
cnn.add(Dropout(0.5))

#Capa clasificadora
#Su salida es la porcion de la imagen que se detecta como
#Semaforo en rojo, verde y amarillo
cnn.add(Dense(clases, activation = 'softmax'))

cnn.compile(loss = 'categorical_crossentropy', optimizer = optimizers.Adam(lr = lr), metrics = ['accuracy'])

cnn.fit(imagen_entrenamiento, nb_epoch = pasos, epochs = epocas, validation_data = imagen_validacion, validation_steps = pasos_validacion)
#------------------------------------------------------

#Guardar el modelo de entrenamiento
"""if not os.path.exists(direccion):
    #Crear la carpeta si se borra o no existe
    os.mkdir(direccion)"""


cnn.save('Modelo/modelo.h5')
cnn.save_weights('Modelo/pesos.h5')

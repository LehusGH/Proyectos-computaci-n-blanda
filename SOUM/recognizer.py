import numpy as np
import keras
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import h5py

longitud, altura = 100, 100

#Acceso a el entrenamiento y los pesos de la red
modelo = './Modelo/modelo.h5'
pesos_modelo = './Modelo/pesos.h5'

#Carga del modelo en la red neuronal y sus respectivos pesos
#cnn = load_model(modelo)
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

#Funcion para leer la imagen y clasificarla segun sus caracteristicas
#En Rojo, Amarillo o Verde
def recognize(image_file):
    x = load_img(image_file, target_size = (longitud, altura))
    x = img_to_array(x)
    x = np.expand_dims(x, axis = 0)
    array = cnn.predict(x)
    resultado = array[0]
    respuesta = np.argmax(resultado)
    if respuesta == 0:
        print('El semáforo está en amarillo')
    elif respuesta == 1:
        print('El semáforo está en rojo')
    elif respuesta == 2:
        print('El semáforo está en verde')
    else:
        print('No se puede reconocer como semáforo')
    return respuesta

recognize('imagen1.jpg')
recognize('imagen2.jpg')
recognize('imagen3.jpg')

import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

longitud, altura = 100, 100

#Acceso a el entrenamiento y los pesos de la red
modelo = './Modelo/modelo.h5'
pesos_modelo = './Modelo/pesos.h5'

#Carga del modelo en la red neuronal y sus respectivos pesos
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
    return respuesta

print(recognize('amarillop.jpg'))
print(recognize('rojop.jpg'))
print(recognize('verdep.jpg'))
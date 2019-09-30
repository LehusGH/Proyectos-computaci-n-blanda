from enfermedades import enfermedades
from enfermedades import sintomas

#Esta lista se usa para enlazar la enfermedad a una lista por medio de
#los numeros usados como clave
#enfermedades -> id_enfermedades
id_enfermedades = {
    0: 'amigdalitis', 1: 'botulismo', 2: 'coronavirus', 3: 'difteria', 
    4: 'ebola', 5: 'escarlatina', 6: 'faringitis', 7: 'gripe', 
    8: 'tuberculosis', 9: 'lepra', 10: 'gonorrea', 11: 'insuficiencia cardiaca', 
    12: 'listeriosis', 13: 'neumonia', 14: 'sepsis', 15: 'urticaria'
}

#Cantidad de enfermedades registradas
n_enfermedades = 16

#Una funcion que debe recibir una lista de enfermedades entregadas por el usuario
#Devuelve una lista de numeros que sirven para detectar la probabillidad
#de padecer alguna enfermedad
def convSintomas(l_sintomas, pos):
    lista_sintomas = enfermedades[id_enfermedades[pos]]
    l_aux = []
    for s in lista_sintomas:
        l_aux.append(sintomas[s])
    #print(l_aux)

    #la cantidad de sintomas sirve para medir la probabilidad de encontrar
    #una enfermedad a partir de unos sintomas
    #la probabilidad P esta dada por
    #P = sintomas acertados / total sintomas enfermedad
    total_sintomas = len(l_aux)
    aciertos = 0
    for s in l_sintomas:
        if l_aux.count(s):
            aciertos += 1
    p = (aciertos / total_sintomas) * 100
    print(id_enfermedades[pos], p, '%')

def consultarEnfermedad(l_sintomas):
    for i in range(n_enfermedades):
        convSintomas(l_sintomas, i)

consultarEnfermedad(['inflamacion', 'ulceras', 'congestion nasal', 'disfagia', 'tos', 'dolor garganta', 'fiebre', 'manchas amigdalas', 'sensibilidad'])
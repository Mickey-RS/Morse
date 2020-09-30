# -*- coding: utf-8 -*-
"""
Created on Sat Jun 6 17:38:02 2020

@author: Mickey
"""

TOLERANCIA = 50.0 #Por ciento
"""Puede ser ajustada, dependiendo del audio que se trabaje!"""

import numpy as np
import wave
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import morse_key as mkey
import contextlib

archivo = 'test.wav'
muestreo, sonido = waves.read(archivo)
# canales: monofónico o estéreo
tamano = np.shape(sonido)
muestras = tamano[0]
m = len(tamano)
canales = 1  # monofónico
if (m>1):  # estéreo
    canales = tamano[1]
# experimento con un canal
if (canales>1):
    canal = 0
    uncanal = sonido[:,canal]
else:
    uncanal = sonido
# rango de observación en segundos
inicia = 0.000
with contextlib.closing(wave.open(archivo,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    termina = frames / float(rate)

"""Aquí le moví para ajustar la duración al audio de prueba que usé"""
# observación en número de muestra
a = int(inicia*muestreo)
b = int(termina*muestreo)
parte = uncanal[a:b]
# Salida # Archivo de audio.wav
print('Descomponiendo a datos. Sea paciente, por favor...')
#waves.write('parte01.wav', muestreo, parte)

orange = []#Serán los datos pasados por el filtro de tolerancia


tol = (max(parte)/100)*TOLERANCIA

print("Tolerancia a ruido: ",tol," dB")#Cantidad

#Guarda sólo los datos que se encuentren por encima del filtro
for data in parte:
    if(abs(data) > tol):
        orange.append(abs(data))
    else:
        orange.append(tol)

#length representa la longitud del silencio en milisegundos
length = 0
green = []#Una nueva lista que guardará sólo los lapsos de sonido y silencio por a parte
previous = tol

for data in orange:
    #Si hay variación en la  frecuencia, hay sonido
    if(data != previous):
        #Se guarda en la nueva gráfica el sonido
        green.append(data)
        length = 0
    else:
        #Luego de 50ms de silencio continuo, se toma como un espacio entre una letra y otra
        if(length > 50):
            green.append(None)
        else:
            green.append(tol)
        length += 1
    previous = data

lengths = []#Representa el número de frecuencias variables continuas, que representan
#La existencia de un sonido
values = []#Guardará el tamaño de cada sonido o silencio registrado
Nones = 0#Llevará el conteo de milisegundos de silencio existentes
for data in green:
    if(data != None):
        #Si el dato no es nulo, añadelo a una lista con frecuencias variables continuas
        #Quiere decir que existe sonido
        lengths.append(data)
        #Y añade el último valor registrado de frecuencias constantes continuas a la lista de valores
        #Se guarda como negativo para reconocer que es un silencio
        values.append(-Nones)
        #Y finalmente resetea el contador de silencio
        Nones = 0
    else:
        #Si se encuentra con datos nulos, se contempla que se ha llegado a un silencio
        #Si el sonido registrado anteriormente dura más de 500ms, se añade a la lista final de valores
        if(len(lengths) > 500):
            values.append(len(lengths))
        #Se cuenta 1ms más al silencio
        Nones += 1
        #Y se resetea la lista de sonido o de frecuencias variables para registrar un nuevo sonido al
        #terminar el silencio actual
        lengths = []

#Un punto vale la mitad de la duración máxima de un sonido
dot = max(values)/2
#Una linea vale la duración máxima de un sonido
line = max(values)
#Cualquier silencio que dure más de la mitad de la duración máxima de un silencio, cuenta como
#un espacio entre letra y letra
minimum = min(values)
notspace = min(values)/2
separator = notspace/2


text = ""
#Se recorre cada valor en la lista y se sustituye por una linea, punto o diagonal
while(0 in values):
    values.remove(0)
for val in values:
    if(val < notspace):
        text+=" \\ "
    elif(val < separator):
        text += " "
    elif((val <= dot) and (val > 0)):
        text+="."
    elif((val <= line) and (val > 0)):
        text+="-"

#Se desencripta a texto por medio de una librería auxiliar
print("\n\n"+text)
print("\n"+mkey.translate(text)+"\n\n")
# Graficamos...
plt.plot(parte)
plt.plot(orange)
plt.plot(green)
plt.show()

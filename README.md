# Decodificador Morse

El programa permite tomar un audio en formato .wav con un mensaje codificado en código morse, decodificarlo y mostrarlo en pantalla, primero traducido a puntos y lineas, y después a texto plano, así como mostrar en una gráfica los valores que se tomaron de la pista de audio.
A su vez, dada la variación en la calidad de la pista de audio que puede ser introducida, se puede ajustar la tolerancia de captura en decibeles, para ignorar todo ruido que sea menor a ese nivel de toleerancia.

Para utilizar, sólo hace falta colocar la pista de audio tipo wave (.wav) en la misma ruta que el script, con el nombre "test", y después correr el script. Al hacer esto, la consola mostrará el audio traducido a texto y la gráfica correspondiente.
Para cambiar el valor de la TOLERANCIA, dirigirse a la primer parte del código, justo antes de la importación de Módulos, y cambiar el valor de la variable TOLERANCIA en porcentaje.

### Librerías usadas para la execución del script:

* wave y contextlib: Obtención de información a cerca del archivo de audio (Frames totales y frecuencia).
* matplotlib.pyplot: Para el manejo de gráficos.
* scipy.io.wavfile: Manipulación del archivo de audio.
* morse_key: Módulo que contiene las claves de traducción morse-alfanumérico. Ya integrado en el proyecto.
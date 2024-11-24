<h1 align="center">Programa para realizar estudios de arco eléctrico</h1>
<!-- De esta forma se coloca el Badge cuando no esta dentro de <p> ![Badge Finalizado](https://img.shields.io/badge/STATUS-FINALIZADO-green)   -->

<p align="center">
  <img src=https://img.shields.io/badge/STATUS-FINALIZADO-GREEN>
</p>

 ![GitHub Org's stars](https://img.shields.io/github/stars/camilafernanda?style=social)

 ## Introducción
 Realiza estudios de arco eléctrico en base a los estándares IEEE 1584-2018 y IEEE 1584-2002

 ## Lenguaje de programación
 EL programa se desarrolló en Python y usando la biblioteca Tkinter para la interfaz gráfica de usuario

 ## Rango del estándar IEEE 1584-2002
 - Voltajes dentro del rango de 208V - 15kV, trifásicos
 - Frecuencia de 50Hz o 60Hz
 - Corriente de corto circuito trifásica simétrica en el rango de 700A a 106kA
 - Equipos aterrizados a tierra y no aterrizados
 - Equipos en gabinete de dimensiones típicas
 - Distancia entre los electrodos "Gap" de 13mm - 152mm
 - Fallas trifásicas

## Rango del estándar IEEE 1584-2018
- Voltajes dentro del rango de 208V - 15kV, trifásicos
- Frecuencia de 50Hz o 60Hz
- Corriente de corto circuito trifásica simétrica
  - 208V - 600V: 500A - 106kA
  - 601V - 15kV: 200A - 65kA
- Distancia entre los electrodos "Gap":
  - 208V - 600V: 6.35mm - 76.2mm (0.25in - 3in)
  - 601V - 15kV: 19.05 mm - 254 mm (0.75in - 10in)
- Distancias de trabajo mayores o igual a 305mm (12in)
- Tiempo de liberación de la falla: Sin límite
- Dimensiones límite del gabinete (usando las dimensiones de gabinete de la versión 2002):
  - Altura o Ancho máximo: 1244.6 mm (49 in)
  - Área abierta máxima: 1.549m2 (2401 in2)
  -	Ancho mínimo: El ancho del gabinete debe de ser 4 veces más grande que la distancia entre los electrodos “Gap”
- Configuración de los electrodos:
  - VCB
  - VCBB
  - HCB
  - VOA
  - HOA
## Guía de instlación
- Descargar el repositorio en cualquier carpeta de tu computadora
- Instalar la biblioteca numpy usando la terminal de Python colocando el siguiente codigo: Pip install numpy
- Ejecutar el archivo principal "main_arco_electrico.py" con cualquier compilador que soporte Python. Sugiero usar Visual Estuio Code para ejecutar el programa
Esto Abrirá la ventana principal como se muestra a continuación
<p align="center">
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Ventana_principal_2018.png>
</p>
Como se puede apreciar en la imagen anterior, Al inicio del programa te pide seleccionar el método de cálculo, donde incialmente se tiene preseleccionado la opción IEEE 1584-2018 y varios datos por defecto.

## Guía de uso de la metodología IEEE 1584-2018
- Paso 1. Ingresar el voltaje del sistema en kV y la corriente de corto circuito en kA. Esto permitirá elegir diferentes configuración de equipo para seleccionar.
- Paso 2. Seleccionar el tipo de equipo a analizar. En base al equipo seleccionado se actualizan automáticamente las variables: Distancia de trabajo, Distancia entre los conductores, la altura (Height), el ancho (Width), la profundidad (Depth). Todos estos en milímetros. 
En caso de tener un equipo diferente se puede ingresar los datos manualmente
- Paso 3. Seleccionar si el equipo será de tipo Cerrado "BOX" o de tipo abierto "OA" y en base a esto elegir las configuraciones de electrodos a analizar: VCB, VCBB, HCB, OA, HOA. Cabe destacar que se pueden elegir varias configuraciones de electrodos a ala vez.
- Paso 4. Hacer clic en el botón "CALCULAR". Esto abrirá la siguiente ventana
<p align="center">
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Ventana_secundaria_2018_1.png>
</p>
- Paso 5. Determinar el tiempo de liberación de la falla (T) en milisegundos, de acuerdo con la corriente de arco (Iarc) mostrada en pantalla y dar clic en el botón calcular. Esto realizará el calculo de la energía incidente (E), el límite de arco eléctrico (AFB), la categoría de Equipo de protección personal (EPP) y la variación de la corriente de arco eléctrico (Iarcmin)
- Paso 6. Realizar nuevamente el paso 6 usando (Iarcmin) para determinar el tiempo de liberación de la falla)
NOTA: En la terminal de salida del compilador se imprimiran el proceso de calculo de forma ordenada como se muestra en la siguiente imagen:
<p align="center">
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2018_1.png>
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2018_2.png>
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2018_3.png>
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2018_4.png>
</p>
## Guía de uso de la metodología IEEE 1584-2018
Al seleccionar la metodología IEEE 1584-2002 se presenta la siguiente ventana
<p align="center">
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Ventana_principal_2002.png>
</p>
- Paso 1. Ingresar el voltaje del sistema en kV y la corriente de corto circuito en kA. Esto permitirá elegir diferentes configuración de equipo para seleccionar.
- Paso 2. Seleccionar el tipo de equipo a analizar. En base al equipo seleccionado se actualizan automáticamente las variables: Distancia de trabajo y Distancia entre los conductores, ambos en milímetros.
- Paso 3. Seleccionar si el equipo está aterrizado a tierra (Grounded), sin aterrizar (Ungrounded), o es de alta resistencia (High resistance)
- Paso 4. Hacer clic en el botón "CALCULAR". Esto abrirá la siguiente ventana
<p align="center">
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Ventana_secundaria_2002_1.png>
</p>
- Paso 5. Determinar el tiempo de liberación de la falla (T) en milisegundos, de acuerdo con la corriente de arco (Iarc) mostrada en pantalla y dar clic en el botón calcular. Esto realizará el calculo de la energía incidente (E), el límite de arco eléctrico (AFB), la categoría de Equipo de protección personal (EPP). La variación de la corriente de arco (Iarcmin) es por defecto del 15% el valor original como lo establece la IEEE 1584-2002
- Paso 6. Realizar nuevamente el paso 6 usando (Iarcmin) para determinar el tiempo de liberación de la falla)
NOTA: En la terminal de salida del compilador se imprimiran el proceso de calculo de forma ordenada como se muestra en la siguiente imagen:
<p align="center">
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2002_1.png>
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2002_2.png>
  <img width=500px src=https://github.com/JJ-Trejo/Arco-Electrico/blob/main/assets/Output_2002_3.png>
</p>

## Disclaimer
El uso de este programa es bajo su propio riesgo. El autor no asume ninguna responsabilidad por el uso indebido o los resultados incorrectos derivados de su aplicación. Aunque se ha diseñado y probado para ofrecer resultados precisos, el programa no garantiza la exactitud de los cálculos o la idoneidad para cualquier propósito en particular. El usuario es el único responsable de verificar la precisión de los resultados antes de su aplicación en cualquier contexto profesional o técnico. El autor no se hace responsable de ningún daño directo, indirecto o consecuente que pudiera derivarse del uso del programa.

## AUTORES
| [<img src="https://avatars.githubusercontent.com/u/134732505?v=4" width=115><br><sub> J.J. Trejo M. </sub>](https://github.com/Yisus-1) |
| :---: |

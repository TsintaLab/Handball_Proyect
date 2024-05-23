# Sistema de captura de flujos de datos multimodales para el análisis de movimientos deportivos.

Para comenzar con el funcionamiento del sistema de captura con el sensor ZED 2i es necesario descargar el SDK, recordar que el desarrollo se realizó con la versión 4.0.6
La información que se encuentra aqui es el desarrollo del software que se elaboró para los sensores ZED 2i que incluye la grabación del video, segmentación de los datos en frames, captura de frames RGB-D, asi como el body tracking, skeleton joints.

La información restante es el procesaiento de los datos, para su análisis, desde scripts para crear videos, depuramiento de los datos, refinamiento y análisis.

Este es el arreglo experimental 

![Arreglo experimental](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Diagrama_DT_2.png)

En donde 
1. Porteria
2. Equipo de computo
3. Sensor ZED2i
4. Display LED
5. Action CAM

Para el funcionamiento del sensor se siguen los siguientes paso:
## Sensor ZED 2i
### Descargar el ZED SDK

- Descargar [ZED SDK](https://www.stereolabs.com/developers/release)

### ZED SDK - SVO Recording

### Build the program
 - Build for [Windows](https://www.stereolabs.com/docs/app-development/cpp/windows/)
 - Build for [Linux/Jetson](https://www.stereolabs.com/docs/app-development/cpp/linux/)

### Grabación del video con el sensor ZED 2i
Para comenzar con la captura de los videos se utilizo el código que esta en:
- Carpeta [svoRecording](https://github.com/TsintaLab/Handball_Proyect/tree/main/svoRecording)

### Body Tracking con el sensor ZED 2i
En donde se hicieron modificaciones al código original del SDK del sensor. Sigue los pasos de compilación en la sección de **Build the program.**

En la siguiente carpeta está el código que se modifico para realizar varios procesamientos:
1. Segmentación de los videos en frames.
2. Selección de una Región de interes.
3. La configuración del número de joints. (38 joints)
4. El body tracking por frames.
5. Guardar los datos RGB
6. Guardar los datos de profundidad.
7. Guardar las coordenas de los joints. X, Y y Z

![38 joints](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Display.png)

## Display LEDs
El dispositivo Display LEDs consta de 9 matrices de focos LEDs de 8x8 lo cuales tienen un controlador MAX7219 se controla con la raspberry pi 3B con un raspbian de 32 bits instalado en una MicroSD de 32 Gb.

![Display LED](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Display.png)

En la siguiente carpeta se encuentra el código para la secuencia de encendido de los 9 cuadrantes.
 - Carpeta [displayLED](https://github.com/TsintaLab/Handball_Proyect/tree/main/displayLED)

## Análisis de datos 

### Creación de videos
En la carpeta [DataAnalysis](https://github.com/TsintaLab/Handball_Proyect/tree/main/DataAnalysis) se encuentran distintos scripts en python, para visualización y análisis de datos que nos ayudan al refinamiento y depuración de la base de datos.

El primer análisis fue la segmentación automática de frames, tomando en cuenta la cantidad que la velocidad de captura es de 60 fps asi que la segmentación dependiendo de la velocidad de tiro de los jugadores fue de 240 a 180 frames, la creación de los videos para el análisis del experto del área se utilizó el script [videoMaker2](https://github.com/TsintaLab/Handball_Proyect/blob/main/DataAnalysis/videoMaker2.py) obteniendo como resultado el siguiente ejemplo [videoJugador1Sec1_Tiro1](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Tiro1.mp4). La primera depuración que se realizó fue manual se analizaron estos videos segmentados y se determinaron una cantidad menor de frames que explica mejor el tiro [videoJugador1Sec1_Tiro1_Segment](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/TiroJ1S1_Region1_Sec1.mp4) el tiro 1 del juagodro1Sec1 queda de 240 frames a 80 frames.

### Análisis visual lateralidad

Para el análisis visual de la lateralidad se utiliza el script [Lateralidad](https://github.com/TsintaLab/Handball_Proyect/blob/main/DataAnalysis/analisis3D_2.py), el lado izquierdo del cuerpo se muestra con color rojo y el lado derecho con el color azul la espina dorsal con el color verde, tenemos el ejemplo en las siguientes animaciones una es con la sección del tiro seleccionada manualmente y la otra con el tiro depurado una vez elminados los frames que no contienen los joints de interes para el análisis de los ángulos:

1. Frames 80
![80Frames](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Tiro1_80.gif)

2. Frames 73
![73Frames](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Tiro1.gif)



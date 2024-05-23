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

![38 joints](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/3DKeypoints.png)

| KEYPOINT INDEX | KEYPOINT NAME         | KEYPOINT INDEX | KEYPOINT NAME           | KEYPOINT INDEX | KEYPOINT NAME             | KEYPOINT INDEX | KEYPOINT NAME           |
|----------------|-----------------------|----------------|-------------------------|----------------|---------------------------|----------------|-------------------------|
| 0              | PELVIS                | 10             | LEFT_CLAVICLE           | 20             | LEFT_KNEE                 | 30             | LEFT_HAND_THUMB_4       |
| 1              | SPINE_1               | 11             | RIGHT_CLAVICLE          | 21             | RIGHT_KNEE                | 31             | RIGHT_HAND_THUMB_4      |
| 2              | SPINE_2               | 12             | LEFT_SHOULDER           | 22             | LEFT_ANKLE                | 32             | LEFT_HAND_INDEX_1       |
| 3              | SPINE_3               | 13             | RIGHT_SHOULDER          | 23             | RIGHT_ANKLE               | 33             | RIGHT_HAND_INDEX_1      |
| 4              | NECK                  | 14             | LEFT_ELBOW              | 24             | LEFT_BIG_TOE              | 34             | LEFT_HAND_MIDDLE_4      |
| 5              | NOSE                  | 15             | RIGHT_ELBOW             | 25             | RIGHT_BIG_TOE             | 35             | RIGHT_HAND_MIDDLE_4     |
| 6              | LEFT_EYE              | 16             | LEFT_WRIST              | 26             | LEFT_SMALL_TOE            | 36             | LEFT_HAND_PINKY_1       |
| 7              | RIGHT_EYE             | 17             | RIGHT_WRIST             | 27             | RIGHT_SMALL_TOE           | 37             | RIGHT_HAND_PINKY_1      |
| 8              | LEFT_EAR              | 18             | LEFT_HIP                | 28             | LEFT_HEEL                 |                |                         |
| 9              | RIGHT_EAR             | 19             | RIGHT_HIP               | 29             | RIGHT_HEEL                |                |                         |


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

Para el análisis visual de la lateralidad se utiliza el script [Lateralidad](https://github.com/TsintaLab/Handball_Proyect/blob/main/DataAnalysis/analisis3D_2.py), el lado izquierdo del cuerpo se muestra con color rojo y el lado derecho con el color azul la espina dorsal con el color verde, tenemos un ejemplo en las siguientes animaciones una es con la sección del tiro seleccionada manualmente que consta de 80 frames y la otra animación es el tiro depurado con 73 frames una vez elminados los frames que no contienen los joints de interes **(["Hip", "Elbow", "Shoulder", "Wrist", "Knee"])** para el análisis de los ángulos:

1. Frames 80
![80Frames](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Tiro1_80.gif)

2. Frames 73
![73Frames](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Tiro1.gif)

### Depuración de frames
Con el script [depurar joints](https://github.com/TsintaLab/Handball_Proyect/blob/main/DataAnalysis/frames_nonan.py) se hace la limpieza de los frames que no contienen los joints clave que son **(["Hip", "Elbow", "Shoulder", "Wrist", "Knee"])** dependiendo la lateralidad dominante "R" Diestro o "L" Zurdo. 

### Refinamiento de los datos
Para el refinamiento de los datos se hace un analisis exhaustivo de los datos depurados y se realizan mediante el script [analisis de datos](https://github.com/TsintaLab/Handball_Proyect/blob/main/DataAnalysis/Analisis_BDHandball.py) con el se obtienen distintos analisis como la **precisión del tiro**, **precisión en cuadrante**, **Nivel: Novato, Medio, Experto**, **Evaluación de los tiros por el experto** y **Lateralidad** de cada jugador y secuencia.

<table>
  <tr>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma1.png" alt="Imagen 1"></td>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma1_2.png" alt="Imagen 2"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma2_1.png" alt="Imagen 3"></td>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma3.png" alt="Imagen 4"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma4_1_Ordenado.png" alt="Imagen 5"></td>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma4_3.png" alt="Imagen 6"></td>
  </tr>
 <tr>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Histograma5.png" alt="Imagen 7"></td>
    <td><img src="https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Boxplot_Niveles.png" alt="Imagen 8"></td>
  </tr>
</table>

## Análisis de las frecuencias de los movimientos mediante angulos y DTW

El script para calcular los ángulos de los joints y obtendremos 3 ángulos distintos, se encuentra en [angulosG1](https://github.com/TsintaLab/Handball_Proyect/blob/main/DataAnalysis/angulosG1.py) ahora el analisis para el DTW, se sigue el siguiente Algoritmo :

### Dynamic Time Warping (DTW) con distancia euclidiana y extracción del Warping Path

#### Pseudocódigo del Algoritmo

```plaintext
Función: DTW_with_path(A, B)
    N <- longitud de la secuencia A
    M <- longitud de la secuencia B
    Crear matriz de costos C[N][M]
    Para i desde 1 hasta N
        Para j desde 1 hasta M
            C[i][j] <- distancia euclidiana entre los puntos A[i] y B[j]
        Fin Para
    Fin Para
    Crear matriz acumulativa D[N][M] inicializada con valores infinitos
    Crear matriz de rutas R[N][M] inicializada con ceros
    D[1][1] <- C[1][1]
    Para i desde 2 hasta N
        D[i][1] <- D[i-1][1] + C[i][1]
    Fin Para
    Para j desde 2 hasta M
        D[1][j] <- D[1][j-1] + C[1][j]
    Fin Para
    Para i desde 2 hasta N
        Para j desde 2 hasta M
            candidates <- {D[i-1][j], D[i][j-1], D[i-1][j-1]}
            min_candidate <- min(candidates)
            D[i][j] <- C[i][j] + min_candidate
            R[i][j] <- índice del candidato en candidates con valor min_candidate
        Fin Para
    Fin Para
    path <- []
    i <- N, j <- M
    Mientras i > 1 o j > 1
        Agregar (i, j) a path
        direction <- R[i][j]
        Si direction = 0
            i <- i - 1
        Sino si direction = 1
            j <- j - 1
        Sino
            i <- i - 1
            j <- j - 1
        Fin Si
    Fin Mientras
    Agregar (1, 1) a path
    retornar D[N][M], path







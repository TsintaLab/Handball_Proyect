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

## Display LEDs

![Arreglo experimental](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Diagrama_DT_2.png)

- Carpeta [BodyTracking](https://github.com/TsintaLab/Handball_Proyect/tree/main/BodyTracking)

## Display LEDs

![Display LED](https://github.com/TsintaLab/Handball_Proyect/blob/main/Figuras/Display.png)

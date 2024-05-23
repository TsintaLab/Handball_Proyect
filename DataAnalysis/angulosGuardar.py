import numpy as np
import os

def leer_coordenadas_desde_archivo(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
        coordenadas = {}
        valores = []
        for linea in lineas[1:]:
            if 'nan' in linea:
                continue

            partes = linea.strip().split(' ')
            nombre_articulacion = partes[0]
            x = float(partes[1].rstrip(','))
            y = float(partes[2].rstrip(','))
            z = float(partes[3])
            coordenadas[nombre_articulacion] = [x, y, z]

    return coordenadas

def calcular_angulo_entre_vectores(U, V):
    producto_punto = np.dot(U, V)
    magnitud_U = np.linalg.norm(U)
    magnitud_V = np.linalg.norm(V)
    
    # Asegurarse de que las magnitudes no sean cero antes de calcular el coseno del ángulo
    if magnitud_U == 0 or magnitud_V == 0:
        return np.nan

    coseno_angulo = np.arccos(producto_punto / (magnitud_U * magnitud_V))
    return np.degrees(coseno_angulo)

# Directorio donde se encuentran los archivos de texto
directorio_tiro = "Frames/Jugador1Sec1/Tiro2/joints/3D_Region_no_nan_El_2"
# Directorio donde se guardarán los archivos de ángulos
directorio_angulos = "Frames/Jugador1Sec1/Tiro2/joints/angulos"

# Crear el directorio de ángulos si no existe
if not os.path.exists(directorio_angulos):
    os.makedirs(directorio_angulos)

# Iterar sobre los archivos en el directorio
for archivo in os.listdir(directorio_tiro):
    if archivo.endswith(".txt"):
        ruta_completa = os.path.join(directorio_tiro, archivo)

        try:
            # Leer las coordenadas desde el archivo
            coordenadas = leer_coordenadas_desde_archivo(ruta_completa)

            # Actualizar las coordenadas de las articulaciones
            R_Shoulder = coordenadas.get('R_Shoulder', [np.nan, np.nan, np.nan])
            R_Elbow = coordenadas.get('R_Elbow', [np.nan, np.nan, np.nan])
            R_Wrist = coordenadas.get('R_Wrist', [np.nan, np.nan, np.nan])
            R_Hip = coordenadas.get('R_Hip', [np.nan, np.nan, np.nan])
            R_Knee = coordenadas.get('R_Knee', [np.nan, np.nan, np.nan])
            print(R_Shoulder)
            # Calcular los vectores U y V para el codo
            U_elbow = np.array(R_Shoulder) - np.array(R_Elbow)
            V_elbow = np.array(R_Wrist) - np.array(R_Elbow)
            angulo_resultado_elbow = calcular_angulo_entre_vectores(U_elbow, V_elbow)

            # Calcular los vectores U y V para el hombro
            U_shoulder = np.array(R_Elbow) - np.array(R_Shoulder)
            V_shoulder = np.array(R_Hip) - np.array(R_Shoulder)
            angulo_resultado_shoulder = calcular_angulo_entre_vectores(U_shoulder, V_shoulder)

            # Calcular los vectores U y V para la cadera
            U_hip = np.array(R_Shoulder) - np.array(R_Hip)
            V_hip = np.array(R_Knee) - np.array(R_Hip)
            angulo_resultado_hip = calcular_angulo_entre_vectores(U_hip, V_hip)

            # Crear un nombre para el archivo de ángulos
            nombre_archivo_angulos = archivo.replace(".txt", "_angulo.txt")
            ruta_archivo_angulos = os.path.join(directorio_angulos, nombre_archivo_angulos)

            # Guardar los ángulos en el archivo de ángulos
            with open(ruta_archivo_angulos, 'w') as f:
                f.write(f"elbow {angulo_resultado_elbow}\n")
                f.write(f"shoulder {angulo_resultado_shoulder}\n")
                f.write(f"hip {angulo_resultado_hip}\n")

            print(f"Archivo de ángulos guardado: {ruta_archivo_angulos}")

        except Exception as e:
            print(f"¡Error al procesar archivo {archivo}: {str(e)}")
            continue


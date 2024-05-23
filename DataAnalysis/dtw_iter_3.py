import os
import numpy as np
from fastdtw import fastdtw
import matplotlib.pyplot as plt

def read_angles_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    angles = {}
    for line in lines:
        joint, angle = line.strip().split()
        angles[joint] = float(angle)
    
    return angles

def read_skeleton_file(file_path):
    data = np.loadtxt(file_path)
    return data

# Ruta de la carpeta que contiene las subcarpetas de los tiros
exp_folder = "BD_Nivel/Novato"

# Listar todas las subcarpetas (tiros) dentro de la carpeta ExpSec1_2
tiro_folders = [folder for folder in os.listdir(exp_folder) if os.path.isdir(os.path.join(exp_folder, folder))]

# Lista para almacenar las medias de las medias de las distancias DTW de cada tiro
mean_mean_distances = []

# Procesar cada tiro
for i, tiro_folder in enumerate(tiro_folders):
    print(f"Procesando tiro {i+1}/{len(tiro_folders)}: {tiro_folder}")
    
    # Ruta de la carpeta que contiene los archivos de ángulos del tiro actual
    angulos_folder = os.path.join(exp_folder, tiro_folder, "joints/angulos")
    
    # Leer todos los archivos de ángulos del tiro actual
    file_paths = [os.path.join(angulos_folder, file) for file in os.listdir(angulos_folder) if file.endswith(".txt")]
    
    # Lista para almacenar las distancias del DTW con otros tiros
    distances_with_others = []
    
    # Procesar archivos de ángulos del tiro actual
    for file_path in file_paths:
        try:
            angles1 = read_angles_file(file_path)
            matrice1 = np.array([[np.cos(np.radians(angle)), np.sin(np.radians(angle))] for angle in angles1.values()])
            
            # Calcular las distancias del DTW con los otros tiros
            distances_to_other_tiros = []
            for j, other_tiro_folder in enumerate(tiro_folders):
                if other_tiro_folder != tiro_folder:
                    # Ruta de la carpeta que contiene los archivos de ángulos del otro tiro
                    other_angulos_folder = os.path.join(exp_folder, other_tiro_folder, "joints/angulos")
                    
                    # Leer todos los archivos de ángulos del otro tiro
                    other_file_paths = [os.path.join(other_angulos_folder, file) for file in os.listdir(other_angulos_folder) if file.endswith(".txt")]
                    
                    # Procesar archivos de ángulos del otro tiro
                    other_distances = []
                    for other_file_path in other_file_paths:
                        try:
                            angles2 = read_angles_file(other_file_path)
                            matrice2 = np.array([[np.cos(np.radians(angle)), np.sin(np.radians(angle))] for angle in angles2.values()])
                            
                            # Calcular la distancia del DTW entre el tiro actual y el otro tiro
                            distance, _ = fastdtw(matrice1, matrice2)
                            other_distances.append(distance)
                        except Exception as e:
                            print(f"Error al procesar archivo: {other_file_path}")
                            print(f"Error: {e}")
                    
                    # Calcular la distancia media del DTW con el otro tiro y agregarla a la lista
                    mean_distance_to_other_tiro = np.mean(other_distances)
                    distances_to_other_tiros.append(mean_distance_to_other_tiro)
            
            # Calcular la media de las distancias del DTW con otros tiros para el tiro actual y agregarla a la lista
            mean_distance_with_others = np.mean(distances_to_other_tiros)
            distances_with_others.append(mean_distance_with_others)
        except Exception as e:
            print(f"Error al procesar archivo: {file_path}")
            print(f"Error: {e}")
    
    # Calcular la media de las distancias del DTW con otros tiros para el tiro actual y agregarla a la lista general
    mean_mean_distance = np.mean(distances_with_others)
    mean_mean_distances.append(mean_mean_distance)

# Crear el gráfico de dispersión (scatter plot)
plt.figure()
plt.scatter(range(1, len(tiro_folders) + 1), mean_mean_distances, color='blue', label='Tiro vs Todos')
plt.axhline(np.mean(mean_mean_distances), color='red', linestyle='dashed', linewidth=2, label=f'Media de Medias: {np.mean(mean_mean_distances):.2f}')
plt.xlabel('Tiro')
plt.ylabel('Media de Medias de Distancias DTW')
plt.title('Media de Medias de Distancias DTW por Medio')
plt.legend()

# Agregar etiquetas a cada punto del gráfico
for i, mean_mean_distance in enumerate(mean_mean_distances):
    plt.text(i + 1, mean_mean_distance, f"Tiro {i + 1}\n{mean_mean_distance:.2f}", fontsize=8, ha='center', va='bottom')

plt.grid()
plt.savefig('Scatter_Medias_Distancias_DTW_por_Novato_2.png', bbox_inches='tight')
plt.show()
# Guardar los resultados en un archivo de texto
output_file_path = "resultados_distancias_todos_Novato_2.txt"
with open(output_file_path, 'w') as output_file:
    output_file.write("Resultados del análisis de DTW para todos los tiros:\n")
    for i, mean_mean_distance in enumerate(mean_mean_distances):
        output_file.write(f"Tiro {i+1}: Media de medias de distancias DTW con otros tiros: {mean_mean_distance}\n")
    output_file.write(f"Media de todas las medias: {np.mean(mean_mean_distances)}\n")

print(f"Resultados guardados en {output_file_path}")

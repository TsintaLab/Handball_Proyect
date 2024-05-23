import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Define la carpeta raíz donde se encuentran las carpetas de los tiros
root_folder = "Frames/Jugador3Sec3"

# Define una función para procesar los datos de una carpeta de un tiro
def process_tiro_folder(tiro_folder):
    folder_path = os.path.join(root_folder, tiro_folder, "joints/3D_Region_no_nan_El_2")
    
    dataframes = []
    nan_data = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Asegúrate de que sean archivos de texto
            file_path = os.path.join(folder_path, filename)
            
            # Leer el archivo y procesar los datos en un DataFrame
            joint_names = []
            x_coordinates = []
            y_coordinates = []
            z_coordinates = []
            
            with open(file_path, 'r') as file:
                next(file)  # Ignorar la primera línea "Keypoints 3D"
                for line in file:
                    parts = line.strip().split(' ')
                    if len(parts) == 4:
                        name = parts[0]
                        x = parts[1].strip().replace(',', ' ')
                        y = parts[2].strip().replace(',', ' ')
                        z = parts[3]
                        joint_names.append(name)
                        x_coordinates.append(x)
                        y_coordinates.append(y)
                        z_coordinates.append(z)
                        if x == 'nan' or y == 'nan' or z == 'nan':
                            nan_data.append((name, x, y, z))
            
            data = {
                "Joint_Name": joint_names,
                "X_Coordinate": x_coordinates,
                "Y_Coordinate": y_coordinates,
                "Z_Coordinate": z_coordinates
            }
            
            df = pd.DataFrame(data)
            dataframes.append(df)
    
    # Crear un DataFrame con los datos "nan"
    nan_df = pd.DataFrame(nan_data, columns=['Joint_Name', 'X_Coordinate', 'Y_Coordinate', 'Z_Coordinate'])
    
    # Generar estadísticas sobre los datos "nan"
    nan_stats = nan_df.describe()
    
    # Plotear un histograma de las frecuencias de "nan" por nombre de joint
    nan_freq_counts = nan_df['Joint_Name'].value_counts()
    return dataframes

# Obtiene la lista de carpetas de los tiros
tiro_folders = os.listdir(root_folder)

# Definir las conexiones entre los joints (personaliza según tu necesidad)
conexiones = [
    ('Pelvis', 'Spine_1'),
    ('Spine_1', 'Spine_2'),
    ('Spine_2', 'Spine_3'),
    ('Spine_3', 'Neck'),
    ('Neck', 'Nose'),
    ('Nose', 'L_Eye'),
    ('L_Eye', 'L_Ear'),
    ('Nose', 'R_Eye'),
    ('R_Eye', 'R_Ear'),
    ('Spine_3', 'L_Clavicle'),
    ('L_Clavicle', 'L_Shoulder'),
    ('L_Shoulder', 'L_Elbow'),
    ('L_Elbow', 'L_Wrist'),
    ('Spine_3', 'R_Clavicle'),
    ('R_Clavicle', 'R_Shoulder'),
    ('R_Shoulder', 'R_Elbow'),
    ('R_Elbow', 'R_Wrist'),
    ('Pelvis', 'L_Hip'),
    ('L_Hip', 'L_Knee'),
    ('L_Knee', 'L_Ankle'),
    ('L_Ankle', 'L_Heel'),
    ('L_Ankle', 'L_Big_Toe'),
    ('L_Ankle', 'L_Small_Toe'),
    ('Pelvis', 'R_Hip'),
    ('R_Hip', 'R_Knee'),
    ('R_Knee', 'R_Ankle'),
    ('R_Ankle', 'R_Heel'),
    ('R_Ankle', 'R_Big_Toe'),
    ('R_Ankle', 'R_Small_Toe')
]

# Definir los colores de las conexiones para las articulaciones R y L
colores_conexiones = {}

# Iterar sobre las conexiones y asignar colores según el prefijo
for joint1, joint2 in conexiones:
    if joint1.startswith('R_') and joint2.startswith('R_'):
        color = 'red'
    elif joint1.startswith('L_') and joint2.startswith('L_'):
        color = 'green'
    else:
        color = 'blue'  # Otros colores para conexiones no especificadas

    colores_conexiones[(joint1, joint2)] = color

# Itera a través de las carpetas de los tiros y crea animaciones y histogramas para cada una
for tiro_folder in tiro_folders:
    if os.path.isdir(os.path.join(root_folder, tiro_folder)):
        dataframes = process_tiro_folder(tiro_folder)
        
        # Crea una figura 3D de Matplotlib
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Inicialización de la animación
        def init():
            ax.clear()
        
        # Función de actualización para la animación
        def update(frame):
            ax.clear()
            df = dataframes[frame]
            x = df['X_Coordinate'].astype(float)
            y = df['Y_Coordinate'].astype(float)
            z = df['Z_Coordinate'].astype(float)
            
            # Reemplazar NaN por valores que no afecten la representación
            x = np.nan_to_num(x, nan=0.0)
            y = np.nan_to_num(y, nan=0.0)
            z = np.nan_to_num(z, nan=0.0)
            # Obtener los colores para los puntos de los joints
            colors = []
            for joint_name in df['Joint_Name']:
                if joint_name.startswith('R_'):
                    colors.append('red')
                elif joint_name.startswith('L_'):
                    colors.append('green')
                else:
                    colors.append('blue')            
            
            # Dibujar los puntos de los joints en 3D
            ax.scatter(x, z, y,c=colors, marker='+',label='Frame {}'.format(frame+1))
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Depth (Z Coordinate)')  # Z como profundidad
            ax.set_zlabel('Height (Y Coordinate)')  # Y como altura
            ax.set_title('Skeleton Joints Frame {}'.format(frame+1))
            ax.set_xlim([-1.5, 1.5])  # Rango fijo en el eje X
            ax.set_ylim([-6, 0])  # Rango fijo en el eje Y
            ax.set_zlim([-1.2, 1.5])  # Rango fijo en el eje Z
            ax.legend()
            # Configurar el aspecto de la gráfica 3D aquí
            # Dibujar las conexiones entre los joints
            for joint1, joint2 in conexiones:
                joint1_data = df[df['Joint_Name'] == joint1]
                joint2_data = df[df['Joint_Name'] == joint2]

                if not joint1_data.empty and not joint2_data.empty:
                    x1, y1, z1 = joint1_data['X_Coordinate'].astype(float).values[0], joint1_data['Y_Coordinate'].astype(float).values[0], joint1_data['Z_Coordinate'].astype(float).values[0]
                    x2, y2, z2 = joint2_data['X_Coordinate'].astype(float).values[0], joint2_data['Y_Coordinate'].astype(float).values[0], joint2_data['Z_Coordinate'].astype(float).values[0]

                    # Obtener el color de la conexión
                    color = colores_conexiones.get((joint1, joint2), 'blue')
                    # Agregar una línea de conexión entre los joints
                    ax.plot([x1, x2], [z1, z2], [y1, y2], color=color)
        # Crear la animación
        ani = FuncAnimation(fig, update, frames=len(dataframes), init_func=init, repeat=False)
        
        # Guardar la animación en un archivo
        animation_output_file = "{}.gif".format(tiro_folder)
        ani.save(animation_output_file, writer='pillow')
        # Cerrar la figura para liberar memoria
        plt.close(fig)



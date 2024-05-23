import os
import pandas as pd
import matplotlib.pyplot as plt

# Define la carpeta raíz donde se encuentran las carpetas de los tiros
root_folder = "Frames/Jugador3Sec3"

# Define una función para procesar los datos de una carpeta de un tiro y exportar los datos del histograma
def process_tiro_folder(tiro_folder, nan_data_all, no_nan_data_all):
    folder_path = os.path.join(root_folder, tiro_folder, "joints/3D_Region")

    nan_data = []
    no_nan_data = []  # Agregar una lista para los registros sin "nan"

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Asegúrate de que sean archivos de texto
            file_path = os.path.join(folder_path, filename)

            # Leer el archivo y procesar los datos en busca de "nan"
            with open(file_path, 'r') as file:
                next(file)  # Ignorar la primera línea "Keypoints 3D"
                for line in file:
                    parts = line.strip().split(' ')
                    if len(parts) == 4:
                        name = parts[0]
                        x = parts[1].strip().replace(',', ' ')
                        y = parts[2].strip().replace(',', ' ')
                        z = parts[3]
                        if x == 'nan' or y == 'nan' or z == 'nan':
                            nan_data.append((name, x, y, z))
                        else:
                            no_nan_data.append((name, x, y, z))  # Agregar a la lista sin "nan"

    # Extender las listas acumulativas con los datos del tiro actual
    nan_data_all.extend(nan_data)
    no_nan_data_all.extend(no_nan_data)

# Crear listas acumulativas para todos los datos
nan_data_all = []
no_nan_data_all = []

# Obtiene la lista de carpetas de los tiros
tiro_folders = os.listdir(root_folder)

# Itera a través de las carpetas de los tiros y acumula los datos
for tiro_folder in tiro_folders:
    if os.path.isdir(os.path.join(root_folder, tiro_folder)):
        process_tiro_folder(tiro_folder, nan_data_all, no_nan_data_all)

# Crear un DataFrame con todos los datos "nan"
nan_df_all = pd.DataFrame(nan_data_all, columns=['Joint_Name', 'X_Coordinate', 'Y_Coordinate', 'Z_Coordinate'])

# Generar estadísticas sobre todos los datos "nan"
nan_stats_all = nan_df_all.describe()

# Crear un histograma de las frecuencias de "nan" por nombre de joint
nan_freq_counts_all = nan_df_all['Joint_Name'].value_counts()

# Crear un DataFrame con todos los datos sin "nan"
no_nan_df_all = pd.DataFrame(no_nan_data_all, columns=['Joint_Name', 'X_Coordinate', 'Y_Coordinate', 'Z_Coordinate'])

# Generar estadísticas sobre todos los datos sin "nan"
no_nan_stats_all = no_nan_df_all.describe()

# Crear un histograma de las frecuencias de los registros sin "nan" por nombre de joint
no_nan_freq_counts_all = no_nan_df_all['Joint_Name'].value_counts()

# Antes de crear las barras, combina las etiquetas de "nan" y "sin nan" y ordena alfabéticamente
combined_labels_all = sorted(set(nan_freq_counts_all.index) | set(no_nan_freq_counts_all.index))

# Asegura que las listas tengan la misma longitud rellenando con 0 donde sea necesario
nan_heights_all = [nan_freq_counts_all.get(label, 0) for label in combined_labels_all]
no_nan_heights_all = [no_nan_freq_counts_all.get(label, 0) for label in combined_labels_all]

# Generar y guardar el histograma de los registros con y sin "nan" apilados
plt.figure(figsize=(12, 6))
ax = plt.subplot(111)

# Crear barras apiladas
width = 0.35
ax.bar(combined_labels_all, nan_heights_all, width, color='lightcoral', label='Con "nan"')
ax.bar(combined_labels_all, no_nan_heights_all, width, color='skyblue', bottom=nan_heights_all, label='Sin "nan"')

plt.xlabel('Nombre del Joint')
plt.ylabel('Frecuencia')
plt.title('Histograma de Frecuencia de Joints Con y Sin "nan" - Todos los Tiros')
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.legend()

# Función para agregar etiquetas a las barras sin solapamiento
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

autolabel(ax.patches)

# Guardar el histograma como una imagen
stacked_histogram_output_file_all = os.path.join("Frames", "Jugador3Sec3_histogram_data_Region", "stacked_histogram_Region_allJ3S3.png")
os.makedirs(os.path.dirname(stacked_histogram_output_file_all), exist_ok=True)
plt.savefig(stacked_histogram_output_file_all)

# Cerrar la figura para liberar memoria
plt.close()

import os
import shutil

# Define la carpeta raíz donde se encuentran las carpetas de los tiros
root_folder = "Frames/Jugador1Sec3"

# Define los joints que deseas analizar
#selected_joints = ["R_Hip", "R_Elbow", "R_Shoulder", "R_Wrist", "R_Knee"]
selected_joints = ["L_Hip", "L_Elbow", "L_Shoulder", "L_Wrist", "L_Knee"]


# Define una función para procesar los datos de una carpeta de un tiro y copiar los archivos sin "nan"
def process_tiro_folder(tiro_folder):
    folder_path = os.path.join(root_folder, tiro_folder, "joints/3D_Region")
    
    # Crear una nueva carpeta para los datos sin "nan"
    output_folder_no_nan = os.path.join(root_folder, tiro_folder, "joints/3D_Region_no_nan_El_2")
    os.makedirs(output_folder_no_nan, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as file:
                lines_without_nan = []
                has_nan = False
                next(file)  # Ignorar la primera línea "Keypoints 3D"
                for line in file:
                    parts = line.strip().split(' ')
                    if len(parts) == 4:
                        name, x, y, z = parts[0], parts[1].strip().replace(',', ' '), parts[2].strip().replace(',', ' '), parts[3]
                        if name in selected_joints and any(coord == 'nan' for coord in [x, y, z]):
                            has_nan = True
                            break
                        lines_without_nan.append(line)

                # Copiar el archivo si no tiene "nan" en los joints seleccionados
                if not has_nan:
                    output_file_no_nan = os.path.join(output_folder_no_nan, filename)
                    with open(output_file_no_nan, 'w') as output_file:
                        output_file.write("Keypoints 3D\n")
                        output_file.writelines(lines_without_nan)

# Ejemplo de uso de la función
# Obtiene la lista de carpetas de los tiros
tiro_folders = os.listdir(root_folder)
# Itera a través de las carpetas de los tiros y copia los archivos sin "nan"
for tiro_folder in tiro_folders:
    if os.path.isdir(os.path.join(root_folder, tiro_folder)):
        process_tiro_folder(tiro_folder)
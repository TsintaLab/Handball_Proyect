import os
import shutil
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define el alcance y las credenciales
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('elated-ranger-392304-b5d69e68f013.json', scope)

# Autentica y crea una instancia del cliente de gspread
client = gspread.authorize(credentials)

# Abre la hoja de cálculo por su ID
spreadsheet = client.open_by_key('1rrmlUMFnyNaOBrrmPXCa52FZ4Frt0r5cSei5j_qQ9vM')

# Obtener una lista de todas las hojas en el documento
sheets = spreadsheet.worksheets()

# Crear un DataFrame vacío para almacenar los datos de todas las hojas
all_data = pd.DataFrame()

# Iterar a través de las hojas y agregar los datos al DataFrame
for i, sheet in enumerate(sheets):
    # Obtener los datos de la hoja actual
    data = sheet.get_all_values()
    
    # Convertir los datos en un DataFrame
    df = pd.DataFrame(data)
    
    # Si no es la primera hoja, quitar la primera fila
    if i != 0:
        df = df[1:]
    
    # Agregar los datos al DataFrame principal
    all_data = pd.concat([all_data, df], ignore_index=True)

# Ajustar las opciones de visualización según tus necesidades
pd.set_option('display.max_columns', None)

# Filtrar las columnas relevantes (Nivel de jugador y Tiro_Index)
filtered_data = all_data[['Nivel de jugador', 'Tiro_Index']]

# Iterar a través de los datos filtrados y copiar las carpetas
for index, row in filtered_data.iterrows():
    nivel = row['Nivel de jugador']
    tiro_index = row['Tiro_Index']
    
    # Ruta de la carpeta de origen
    carpeta_origen = f'Frames\\ExpSec1\\{nivel}\\{tiro_index}'
    
    # Ruta de la carpeta de destino
    carpeta_destino = f'Frames\\{nivel}\\{tiro_index}'
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Copiar los archivos de la carpeta de origen a la carpeta de destino
    for archivo in os.listdir(carpeta_origen):
        ruta_origen = os.path.join(carpeta_origen, archivo)
        ruta_destino = os.path.join(carpeta_destino, archivo)
        shutil.copy(ruta_origen, ruta_destino)
        print(f"Copiado: {ruta_origen} -> {ruta_destino}")

print("Proceso completado. Las carpetas han sido copiadas según el nivel y el índice del tiro.")

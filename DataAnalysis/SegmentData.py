from tqdm import tqdm

def segmentar_archivo(archivo, cadena_delimitadora):
    try:
        with open(archivo, 'r', encoding="utf-8") as archivo_original:
            contenido = archivo_original.read()
            segmentos = contenido.split(cadena_delimitadora)
            
            # Guardar cada segmento en un nuevo archivo
            for i, segmento in tqdm(enumerate(segmentos), desc="Procesando", unit="n"):
                nombre_archivo_segmento = f'Frames/Jugador3Sec3_2/Ske_{i}.txt'
                with open(nombre_archivo_segmento, 'w') as archivo_segmento:
                    archivo_segmento.write(segmento)
                    
        print(f'Archivo segmentado en {len(segmentos)} segmentos.')
        
    except FileNotFoundError:
        print(f'El archivo {archivo} no existe.')

# Llamar a la función para segmentar el archivo
nombre_archivo = 'G:\Mi unidad\Doctorado IA\BaseHandball\Frames\Jugador3Sec3_2\Data.txt'  # Reemplaza con el nombre de tu archivo
cadena_delimitadora = 'frame'     # Reemplaza con tu cadena delimitadora
segmentar_archivo(nombre_archivo, cadena_delimitadora)

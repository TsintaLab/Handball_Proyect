import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shutil
from tqdm import tqdm
import sys


# Abre un archivo para escribir
sys.stdout = open('resultados.txt', 'w')
############## Cargar la Base desde google Sheets y combinar todas las hojas en un solo data Frame ###########
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

# Ajustar las opciones de visualización de pandas para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

all_data.columns = all_data.iloc[0]
all_data= all_data[1:]
# Imprimir el DataFrame completo
#print(all_data['No_Frames'].to_string(index=False))
###########################################################################################################

################################# Analisis 1.- Variable Entro o no a porteria [0 - 1] ######################################################################
print("##################################################")
print("Analisis 1.- Variable Entro o no a porteria [0 - 1]")
print("##################################################\n")
# Convertir la columna 'Entro a porteria' a tipo booleano
all_data['Entro a porteria'] = all_data['Entro a porteria'].astype(int)

# Filtrar los tiros donde 'Entro a porteria' es igual a 10
all_data_filtrado = all_data[all_data['Entro a porteria'] != 10]

# Contar cuántos tiros entraron y cuántos no después de filtrar
tiros_entraron = all_data_filtrado['Entro a porteria'].sum()
tiros_no_entraron = all_data_filtrado['Entro a porteria'].count() - tiros_entraron

# Imprimir los resultados
print(f"Total de tiros que entraron: {tiros_entraron}")
print(f"Total de tiros que no entraron: {tiros_no_entraron}")
# Calcular el porcentaje de tiros que entraron
porcentaje_entraron = (tiros_entraron / all_data_filtrado['Entro a porteria'].count()) * 100
# Imprimir el resultado
print(f"Porcentaje de tiros que entraron: {porcentaje_entraron:.2f}%")

# Obtener estadísticas básicas de la variable 'Entro a porteria'
estadisticas_entro = all_data_filtrado['Entro a porteria'].describe()

# Crear un DataFrame con el conteo de tiros que entraron y no entraron por jugador
conteo_entro_no_entro = all_data.groupby('Index')['Entro a porteria'].value_counts().unstack(fill_value=0)

# Agregar una columna al DataFrame para el porcentaje de tiros que entraron
conteo_entro_no_entro['Porcentaje_Entraron'] = conteo_entro_no_entro[1] / (conteo_entro_no_entro[1] + conteo_entro_no_entro[0] + conteo_entro_no_entro[10]) * 100
# Ordenar el DataFrame por la columna de porcentaje de tiros que entraron de mayor a menor
conteo_entro_no_entro_sorted = conteo_entro_no_entro.sort_values(by='Porcentaje_Entraron', ascending=False)
# Imprimir las estadísticas
print("Estadísticas de 'Entro a porteria':")
print(estadisticas_entro)

# Agrupar por jugador y calcular la proporción de tiros que entraron para cada uno
proporcion_entro_por_jugador = all_data_filtrado.groupby('Index')['Entro a porteria'].mean()
# Ordenar las proporciones por jugador de mayor a menor
proporcion_entro_por_jugador_ordenada = proporcion_entro_por_jugador.sort_values(ascending=False)
# Eliminar la columna 'Porcentaje_Entraron' antes de crear el gráfico
conteo_entro_no_entro_sin_porcentaje = conteo_entro_no_entro_sorted.drop('Porcentaje_Entraron', axis=1)
# Imprimir las proporciones ordenadas por jugador
print("Proporción de tiros que entraron por jugador (ordenadas de mayor a menor):")
print(proporcion_entro_por_jugador_ordenada)
print("Conteo de tiros: ")
print(conteo_entro_no_entro_sorted)
##################################### 1.1 .- Gráfico Histograma #####################################################
# Crear un gráfico de barras apiladas sin la columna de porcentaje
plt.figure(figsize=(12, 6))
bar_plot = conteo_entro_no_entro_sin_porcentaje.plot(kind='bar', stacked=True, color=['lightcoral', 'lightgreen', 'lightblue'])
plt.title('Conteo de Tiros por Categoría (0, 1, 10) por Jugador (Ordenado)')
plt.xlabel('Jugador')
plt.ylabel('Conteo de Tiros')
plt.xticks(rotation=45, ha='right')

# Agregar etiquetas con la cantidad de cada barra
for i, (v0, v1, v10) in enumerate(zip(conteo_entro_no_entro_sin_porcentaje[0], conteo_entro_no_entro_sin_porcentaje[1], conteo_entro_no_entro_sin_porcentaje[10])):
    # Etiqueta para la categoría '0'
    if v0 > 0:
        bar_plot.text(i, v0 / 2, '0', ha='center', va='center', color='white', fontsize=8)
    # Etiqueta para la categoría '1'
    if v1 > 0:
        bar_plot.text(i, v0 + v1 / 2, '1', ha='center', va='center', color='white', fontsize=8)
    if v10 > 0:
        bar_plot.text(i, v0 + v1 + v10 / 2, '10', ha='center', va='center', color='white', fontsize=8)
    # Total hasta arriba de la barra
    total = v0 + v1 + v10
    bar_plot.text(i, total, str(total), ha='center', va='bottom', color='black', fontsize=8)
# Mostrar el gráfico
plt.grid()
plt.legend(title='Categoría', bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.show()
plt.savefig('Histograma1.png', bbox_inches='tight')
###############################################################################################################
##################################### 1.1.1 .- Gráfico Histograma #####################################################
# Crear un histograma de las proporciones de tiros que entraron por jugador
plt.figure(figsize=(12, 6))
histogram_plot = sns.histplot(x=conteo_entro_no_entro_sorted['Porcentaje_Entraron'], bins=20, kde=True)
plt.title('Histograma del Porcentaje de Tiros que Entraron por Jugador (Ordenado)')
plt.xlabel('Porcentaje de Tiros que Entraron')
plt.ylabel('Frecuencia')
# Añadir líneas guía para la media y la mediana
media = conteo_entro_no_entro_sorted['Porcentaje_Entraron'].mean()
mediana = conteo_entro_no_entro_sorted['Porcentaje_Entraron'].median()
plt.axvline(x=media, color='red', linestyle='--', label=f'Media: {media:.2f}%')
plt.axvline(x=mediana, color='green', linestyle='--', label=f'Mediana: {mediana:.2f}%')
# Mostrar la leyenda
plt.legend()
# Añadir etiquetas
plt.xlabel('Porcentaje de Tiros que Entraron')
plt.ylabel('Frecuencia')
plt.grid()
#plt.show()
plt.savefig('Histograma1_1.png', bbox_inches='tight')
##################################### 1.2 .- Gráfico Boxplot #####################################################
# Crear un box plot de las proporciones de tiros que entraron por jugador
plt.figure(figsize=(12, 6))
box_plot_proporcion_entro = sns.boxplot(x=proporcion_entro_por_jugador_ordenada.index, y=proporcion_entro_por_jugador_ordenada)
plt.title('Distribución de Proporciones de Tiros que Entraron por Jugador')
plt.xlabel('Jugador')
plt.ylabel('Proporción de Tiros que Entraron')
plt.xticks(rotation=90)  # Rotar etiquetas para mayor claridad
# Añadir puntos para cada observación en el box plot
sns.swarmplot(x=proporcion_entro_por_jugador.index, y=proporcion_entro_por_jugador, color='black', size=4)
# Agregar líneas guía para la media y la mediana
media = proporcion_entro_por_jugador.mean()
mediana = proporcion_entro_por_jugador.median()
plt.axhline(y=media, color='red', linestyle='--', label=f'Media: {media:.2%}')
plt.axhline(y=mediana, color='green', linestyle='--', label=f'Mediana: {mediana:.2%}')
# Mostrar la leyenda
plt.legend()
plt.grid()
#plt.show()
plt.savefig('Histograma1_2.png', bbox_inches='tight')
###########################################################################################################
#####################2.- Precisión Seccion indicada y seccion en donde entro #############################################
print("##################################################")
print("Analisis 2.- Precisión Seccion indicada y seccion en donde entro")
print("##################################################\n")
# Convertir las columnas relevantes a tipo numérico para facilitar la comparación
all_data['Seccion indicada'] = pd.to_numeric(all_data['Seccion indicada'], errors='coerce')
all_data['Sección donde entro'] = pd.to_numeric(all_data['Sección donde entro'], errors='coerce')
# Filtrar las filas donde las columnas coinciden
coincidencias = all_data[all_data['Seccion indicada'] == all_data['Sección donde entro']]

# Contar el número de coincidencias
cantidad_coincidencias = len(coincidencias)

# Imprimir el resultado
print(f"Número de coincidencias entre Sección indicada y Sección donde entro: {cantidad_coincidencias}")

# Contar el total de tiros
total_tiros = all_data['Tiro'].count()

# Imprimir el resultado
print(f"Total de Tiros: {total_tiros}")
print(f"Porcentaje de aciertos: {(cantidad_coincidencias/total_tiros)*100}")

# Crear una columna para indicar si las secciones coinciden
all_data['Coinciden'] = all_data['Seccion indicada'] == all_data['Sección donde entro']

# Contar las coincidencias por jugador
coincidencias_por_jugador = all_data.groupby('Index')['Coinciden'].sum()
total_tiros_por_jugador = all_data.groupby('Index')['Coinciden'].count()

# Calcular el porcentaje de coincidencias
porcentaje_coincidencias_por_jugador = (coincidencias_por_jugador / total_tiros_por_jugador) * 100

# Ordenar los resultados de mayor a menor
coincidencias_por_jugador = coincidencias_por_jugador.sort_values(ascending=False)

porcentaje_coincidencias_por_jugador = porcentaje_coincidencias_por_jugador.sort_values(ascending=False)

# Crear un DataFrame con los resultados
resultados = pd.DataFrame({
    'Coincidencias': coincidencias_por_jugador,
    'Total Tiros': total_tiros_por_jugador,
    'Porcentaje Coincidencias': porcentaje_coincidencias_por_jugador
})

# Ordenar los resultados de mayor a menor por el porcentaje de coincidencias
resultados = resultados.sort_values(by='Porcentaje Coincidencias', ascending=False)
# Crear una variable para las no coincidencias
no_coincidencias_por_jugador = resultados['Total Tiros'] - resultados['Coincidencias']
# Imprimir el resultado
print("Número de coincidencias, total de tiros y porcentaje de coincidencias por jugador (ordenado de mayor a menor):")
print(resultados)
######################### 2.1 .-  Graficos #############################################
# Gráfico de barras apilado para mostrar coincidencias y no coincidencias por jugador
plt.figure(figsize=(12, 6))
jugadores = resultados.index
bar_width = 0.8  # Ancho de las barras
# Plotear las barras de "Coincidencias" sobre las anteriores
plt.bar(jugadores, resultados['Coincidencias'], color='skyblue', label='Coincidencias')
# Plotear las barras de "No Coincidencias" sobre las anteriores
plt.bar(jugadores, no_coincidencias_por_jugador, bottom=resultados['Coincidencias'], color='lightcoral', label='No Coincidencias', alpha=0.7)
plt.title('Coincidencias y No Coincidencias por Jugador')
plt.xlabel('Jugador')
plt.ylabel('Cantidad')
plt.xticks(rotation=90)  # Rotar etiquetas para mayor claridad
# Agregar etiquetas a las barras
for i, (coincidencias, no_coincidencias) in enumerate(zip(resultados['Coincidencias'], no_coincidencias_por_jugador)):
    plt.text(i, coincidencias/2, str(coincidencias), ha='center', va='center')
    plt.text(i, coincidencias + no_coincidencias/2, str(no_coincidencias), ha='center', va='center', color='blue')
# Añadir leyenda
plt.legend()
plt.grid()
#plt.show()
plt.savefig('Histograma2.png', bbox_inches='tight')
########################### 2.2 .-  Graficos #########################
# Gráfico de barras para mostrar el porcentaje de coincidencias por jugador
plt.figure(figsize=(12, 6))
porcentaje_coincidencias_por_jugador.plot(kind='bar', color='mediumseagreen')
plt.title('Porcentaje de Coincidencias por Jugador')
plt.xlabel('Jugador')
plt.ylabel('Porcentaje de Coincidencias')
plt.xticks(rotation=90)  # Rotar etiquetas para mayor claridad
# Agregar etiquetas a las barras
for i, v in enumerate(porcentaje_coincidencias_por_jugador):
    plt.text(i, v + 0.1, f'{v:.2f}%', ha='center', va='bottom')

plt.grid()
#plt.show()
plt.savefig('Histograma2_1.png', bbox_inches='tight')
################################################################################################################################
##################### 3. Nivel de Jugador [Novato, Medio, Experto] ###########################################################3
print("##################################################")
print("Analisis 3.- Nivel de Jugador [Novato, Medio, Experto]")
print("##################################################\n")
# Contar cuántos jugadores tienen nivel novato, medio y experto
nivel_counts = all_data['Nivel de jugador [1,2,3] (novato, medio, experto)'].value_counts()

# Obtener el número de jugadores en cada nivel
jugadores_novato = nivel_counts.iloc[2]
jugadores_medio = nivel_counts.iloc[1]
jugadores_experto = nivel_counts.iloc[0]

# Etiquetas y valores para el gráfico
niveles = ['Novato', 'Medio', 'Experto']
jugadores = [jugadores_novato, jugadores_medio, jugadores_experto]

# Imprimir los resultados
print(f"Jugadores Nivel Novato: {jugadores_novato}")
print(f"Jugadores Nivel Medio: {jugadores_medio}")
print(f"Jugadores Nivel Experto: {jugadores_experto}")
#################### 3.1 .- Grafica ####################################################
# Crear el gráfico de barras
plt.figure(figsize=(12, 6))
plt.bar(niveles, jugadores, color=['blue', 'orange', 'green'])
# Agregar números sobre las barras
for i, valor in enumerate(jugadores):
    plt.text(i, valor + 0.1, str(valor), ha='center', va='bottom')
plt.title('Distribución de jugadores por nivel')
plt.xlabel('Nivel de jugador')
plt.ylabel('Número de jugadores')
plt.grid()
#plt.show()
plt.savefig('Histograma3.png', bbox_inches='tight')
######################################################################################################################
##################### 4. Nivel del Tiro [0 -10] ###########################################################3
print("##################################################")
print("Analisis 4. Nivel del Tiro [0 -10]")
print("##################################################\n")
# Nivel de tiro data
nivel_tiro_data = all_data['Nivel del tiro [0 -10]'].astype(float)  # Asegúrate de que los datos sean de tipo float

# Realizar análisis estadístico
media = nivel_tiro_data.mean()
mediana = nivel_tiro_data.median()
moda = nivel_tiro_data.mode()[0]
rango = nivel_tiro_data.max() - nivel_tiro_data.min()
desviacion_estandar = nivel_tiro_data.std()
cuartil_1 = nivel_tiro_data.quantile(0.25)
cuartil_2 = nivel_tiro_data.quantile(0.50)
cuartil_3 = nivel_tiro_data.quantile(0.75)

# Imprimir los resultados
print(f"Media: {media}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")
print(f"Rango: {rango}")
print(f"Desviación Estándar: {desviacion_estandar}")
print(f"Cuartil 1: {cuartil_1}")
print(f"Cuartil 2 (Mediana): {cuartil_2}")
print(f"Cuartil 3: {cuartil_3}")

# También puedes utilizar describe() para obtener un resumen estadístico más completo
resumen_estadistico = nivel_tiro_data.describe()
print(resumen_estadistico)


# Contar cuántos jugadores tienen nivel novato, medio y experto
nivelTiro_counts = all_data['Nivel del tiro [0 -10]'].value_counts()
# Obtener el número de jugadores en cada nivel
Tiros = nivelTiro_counts
print(Tiros)
############## 4.1 .- Graficos Histograma ##########################################
# Histograma
plt.figure(figsize=(10, 6))
sns.histplot(nivel_tiro_data, bins=20, kde=True, color='skyblue')
plt.title('Histograma del Nivel de Tiro')
plt.xlabel('Nivel del Tiro [0 - 10]')
plt.ylabel('Frecuencia')
plt.grid(axis='both', linestyle='--', alpha=0.7)  # Agregar cuadrícula en ambos ejes
plt.xlim(0, 10)  # Establecer límites del eje x de 0 a 10
#plt.show()
plt.savefig('Histograma4.png', bbox_inches='tight')
############## 4.2 .- Graficos Boxplot ##########################################
# Convertir la columna 'Nivel del tiro [0 -10]' a tipo numérico
all_data['Nivel del tiro [0 -10]'] = pd.to_numeric(all_data['Nivel del tiro [0 -10]'], errors='coerce')

# Obtener el orden de los jugadores según la mediana del nivel de tiro
orden_jugadores = all_data.groupby('Index')['Nivel del tiro [0 -10]'].median().sort_values(ascending=False).index

# Boxplot agrupado por jugador con etiquetas rotadas y media como línea
plt.figure(figsize=(12, 8))
box_plot = sns.boxplot(data=all_data, x='Index', y='Nivel del tiro [0 -10]', order=orden_jugadores, 
                       color='lightcoral', 
                       boxprops=dict(alpha=0.5),  # Hacer las cajas transparentes
                       meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black'), 
                       medianprops={'color':'black'},
                       meanline=True)  # Mostrar la línea de la media

# Fijar ticks y rotar etiquetas del eje x
ticks = range(len(all_data['Index'].unique()))
plt.xticks(ticks, orden_jugadores, rotation=45, ha="right")

plt.title('Boxplot del Nivel de Tiro Agrupado por Jugador (Ordenado)')
plt.xlabel('Jugador')
plt.ylabel('Nivel del Tiro [0 - 10]')
plt.grid(linestyle='--', alpha=0.7)
plt.savefig('Histograma4_1_Ordenado.png', bbox_inches='tight')
plt.show()
############## 4.3 .- Graficos Histograma ##########################################
# Lista de jugadores únicos
jugadores_unicos = all_data['Index'].unique()

# Histograma agrupado por jugador con etiquetas
plt.figure(figsize=(12, 8))
for jugador in jugadores_unicos:
    jugador_data = all_data[all_data['Index'] == jugador]
    sns.histplot(data=jugador_data, x='Nivel del tiro [0 -10]', bins=20, kde=True, label=f'Jugador {jugador}')

plt.title('Histograma del Nivel de Tiro por Jugador')
plt.xlabel('Nivel del Tiro [0 - 10]')
plt.ylabel('Frecuencia')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.xlim(0, 10)  # Establecer límites del eje x de 0 a 10
#plt.show()
plt.savefig('Histograma4_2.png', bbox_inches='tight')
############## 4.4 .- Graficos Histograma ##########################################
# Graficar la distribución de niveles de tiro
plt.figure(figsize=(8, 6))
bar_plot = Tiros.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribución de Niveles de Tiro')
plt.xlabel('Nivel de Tiro [0 - 10]')
plt.ylabel('Número de Jugadores')
# Agregar etiquetas con la cantidad de cada barra
for i, v in enumerate(Tiros):
    bar_plot.text(i, v + 0.1, str(v), ha='center', va='bottom')
plt.grid()
#plt.show()
plt.savefig('Histograma4_3.png', bbox_inches='tight')
##################################################################################################################
##################### 5. Brazo [0 - 1] Izquiero, derecho ###########################################################3
print("##################################################")
print("Analisis 5. Brazo [0 - 1] Izquiero, derecho")
print("##################################################\n")
# Contar cuántos jugadores hay para cada brazo
brazo_counts = all_data['Brazo [0,1] izquierdo, derecho'].value_counts()

# Obtener el número de jugadores para cada brazo
jugadores_izquierdo = brazo_counts.iloc[1]
jugadores_derecho = brazo_counts.iloc[0]
# Calcular porcentaje de jugadores para cada brazo
porcentaje_izquierdo = (jugadores_izquierdo / len(all_data)) * 100
porcentaje_derecho = (jugadores_derecho / len(all_data)) * 100


# Imprimir los resultados
print(f"Jugadores con Brazo Izquierdo: {brazo_counts.iloc[1]}")
print(f"Jugadores con Brazo Derecho: {brazo_counts.iloc[0]}")

# Imprimir los resultados con porcentajes
print(f"Jugadores con Brazo Izquierdo: {jugadores_izquierdo} ({porcentaje_izquierdo:.2f}%)")
print(f"Jugadores con Brazo Derecho: {jugadores_derecho} ({porcentaje_derecho:.2f}%)")
############## 5.1 .- Graficos Histograma ##########################################
# Graficar la distribución de jugadores por brazo
plt.figure(figsize=(8, 6))
brazo_plot = brazo_counts.sort_index().plot(kind='bar', color=['skyblue', 'lightgreen'], edgecolor='black')
plt.title('Distribución de Jugadores por Brazo')
plt.xlabel('Brazo (0: Izquierdo, 1: Derecho)')
plt.ylabel('Número de Jugadores')
plt.xticks(rotation=0)
# Agregar etiquetas con la cantidad de cada barra
for i, v in enumerate(brazo_counts.sort_index()):
    brazo_plot.text(i, v + 0.1, str(v), ha='center', va='bottom')
#plt.show()
plt.savefig('Histograma5.png', bbox_inches='tight')
##################################################################################################################
print("##################################################")
print("Analisis 6. No de Frames de cada Tiro")
print("##################################################\n")
# Convertir la columna No_Frames a enteros
all_data['No_Frames'] = all_data['No_Frames'].astype(int)

# Sumar  la columna No_Frames agrupando por jugador
suma_por_jugador = all_data.groupby('Index')['No_Frames'].sum()
# Sumar la columna No_Frames
suma_vertical = all_data['No_Frames'].sum()
# Imprimir el resultado
print(f"Suma vertical de la columna No_Frames después de la conversión a enteros: {suma_vertical}")
# Imprimir el resultado
print("Suma de la columna No_Frames por jugador:")
print(suma_por_jugador)

# Calcular estadísticas descriptivas agrupadas por jugador
estadisticas_por_jugador = all_data.groupby('Index')['No_Frames'].describe()

# Imprimir resultados
print("Estadísticas descriptivas agrupadas por jugador:")
print(estadisticas_por_jugador)
# Cierra el archivo al final
sys.stdout.close()

#######################3 Grafico 6.1 ####################################
frames_por_jugador = all_data.groupby('Index')['No_Frames'].sum()

# Crea un histograma
plt.figure(figsize=(12, 6))
histogram_plot = plt.bar(frames_por_jugador.index, frames_por_jugador, color='skyblue')

# Agrega etiquetas y título
plt.title('Histograma de Frames Agrupados por Jugador')
plt.xlabel('Jugador')
plt.ylabel('Total de Frames')
# Gira las etiquetas del eje X
plt.xticks(rotation=45, ha='right')
# Muestra el valor de cada barra
for barra in histogram_plot:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')


# Muestra el gráfico
plt.grid()
#plt.show()
plt.savefig('Histograma6.png', bbox_inches='tight')

##########################################################################################################################################
# Agrupa por jugador y cuenta el número de tiros
tiros_por_jugador = all_data.groupby('Index')['Tiro'].count()

# Crea un histograma
plt.figure(figsize=(12, 6))
histogram_plot = plt.bar(tiros_por_jugador.index, tiros_por_jugador, color='lightblue')

# Agrega etiquetas y título
plt.title('Histograma del Número de Tiros por Jugador')
plt.xlabel('Jugador')
plt.ylabel('Número de Tiros')

# Gira las etiquetas del eje X
plt.xticks(rotation=45, ha='right')

# Muestra el valor de cada barra
for barra in histogram_plot:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

# Muestra el gráfico
plt.grid()
#plt.show()
plt.savefig('Histograma7.png', bbox_inches='tight')
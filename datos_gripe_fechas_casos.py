# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:49:45 2024

@author: Elena
"""

import pandas as pd # data processing, CSV file
import matplotlib.pyplot as plt

#Leemos el archivo CSV
ruta_archivo_csv_gripe='C:/Users/Elena/Desktop/TFG/mes 1/datos/Vigil_ncia_sindr_mica_d_infeccions_a_Atenci__Prim_ria__Dades_di_ries__20240416_gripe.csv'
datos_gripe_ordenado=pd.read_csv(ruta_archivo_csv_gripe)

# Configurar el tamaño de la fuente y la familia de fuentes
plt.rcParams.update({'font.size': 20, 'font.family': 'Arial'})


datos_gripe_ordenado.set_index('data', inplace=True)
datos_gripe_ordenado.index = pd.to_datetime(datos_gripe_ordenado.index)

datos_csv_gripe_agrupado = datos_gripe_ordenado['casos'].resample('D').sum()

# Crear un nuevo DataFrame con fechas y casos diarios
datos_gripe= pd.DataFrame({'fecha': datos_csv_gripe_agrupado.index, 'casos': datos_csv_gripe_agrupado.values})

datos_gripe.set_index('fecha', inplace=True)
datos_gripe.index = pd.to_datetime(datos_gripe.index)

ruta_archivo_gripe_fechas_casos='C:/Users/Elena/Desktop/TFG/mes 1/datos/datos_gripe_fechas_casos.csv'
datos_gripe.to_csv(ruta_archivo_gripe_fechas_casos)

# Crear la gráfica de la serie temporal
plt.figure(figsize=(12, 6)) 
plt.plot(datos_gripe.index, datos_gripe['casos'], color='blue', linewidth=0.5)  # Crear la línea de la serie temporal
plt.title('Time Series of Influenza Cases', fontsize=22) 
plt.xlabel('Date')  # Etiqueta del eje x
plt.ylabel('Influenza Cases')  # Etiqueta del eje y
plt.grid(True)  # Mostrar la cuadrícula
plt.tight_layout()  # Ajustar el diseño
plt.show()  # Mostrar la gráfica

# Hacer zoom en una región específica
plt.figure(figsize=(20, 6))
plt.plot(datos_gripe.index, datos_gripe.values, marker='o', linestyle='-', color='r')
plt.title('Zoom in on a Specific Region', fontsize=22)
plt.xlabel('Date')
plt.ylabel('Influenza Cases')
plt.grid(True)
plt.tight_layout()
# Establecer los límites del eje x y del eje y para hacer zoom
plt.xlim(pd.to_datetime('2015-01-25'), pd.to_datetime('2015-03-01'))  # Cambiar estos valores según la región que desees hacer zoom
plt.ylim(0, 5000)  # Cambiar estos valores según la región que desees hacer zoom

# Mostrar el gráfico con zoom
plt.show()


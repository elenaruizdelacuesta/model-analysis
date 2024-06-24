# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 21:55:40 2024

@author: Elena
"""

import pandas as pd # data processing, CSV file
import matplotlib.pyplot as plt

# Leemos el archivo CSV de la gripe (podríamos hacer que leyese ya el archivo de gripe agrupado para evitar más lineas, hay que mirarlo)
ruta_archivo_csv_gripe='C:/Users/Elena/Desktop/TFG/mes 1/datos/Vigil_ncia_sindr_mica_d_infeccions_a_Atenci__Prim_ria__Dades_di_ries__20240416_gripe.csv'
datos_gripe_ordenado=pd.read_csv(ruta_archivo_csv_gripe)


ruta_archivo_pob='C:/Users/Elena/Desktop/TFG/mes 1/datos/Registre_central_de_poblaci__del_CatSalut__poblaci__per__rea_b_sica_de_salut_20240514.csv'
data_pob=pd.read_csv(ruta_archivo_pob, dtype={'any': 'int32', 'Regió Sanitària': 'object'}, low_memory=False)

# Nos aseguramos de que la columna 'data' del dataframe de gripe está en formato de fecha
datos_gripe_ordenado.set_index('data', inplace=True)
# Convertir explícitamente el índice a DatetimeIndex
datos_gripe_ordenado.index = pd.to_datetime(datos_gripe_ordenado.index)

# Reorganizamos y sumamos los casos diarios
datos_gripe_agrupado = datos_gripe_ordenado['casos'].resample('D').sum()

# Crear un nuevo DataFrame con fechas y casos diarios
datos_gripe= pd.DataFrame({'fecha': datos_gripe_agrupado.index, 'casos': datos_gripe_agrupado.values})

# Nos aseguramos de que la columna 'fecha' del dataframe de gripe está en formato de fecha
datos_gripe.set_index('fecha', inplace=True)
# Convertir explícitamente el índice a DatetimeIndex
#datos_gripe.index = pd.to_datetime(datos_gripe.index) Hace falta?

# Ahora lo hacemos con casos suavizados
datos_gripe['casos_suavizados']=datos_gripe['casos'].rolling(window=7, center=True, min_periods=1).mean()

# Obtenemos la población total de Cataluña
pob_total_cat=data_pob.groupby('any')['població oficial'].sum()

# Crear un DataFrame para almacenar los resultados
resultados_incidencia = []
# Filtrar el DataFrame para incluir solo los datos de gripe a partir de 2012
datos_gripe = datos_gripe[(datos_gripe.index.year >= 2012) & (datos_gripe.index.year <= 2024)]

for year, group in datos_gripe.groupby(datos_gripe.index.year):
    poblacion_total = pob_total_cat.loc[year]
    group['incidencia']=100000*(group['casos_suavizados']/poblacion_total)
    # Agregar los resultados al DataFrame de resultados
    #resultados_incidencia = pd.concat([resultados_incidencia, group]) ????
    resultados_incidencia.append(group)

# Concatenar todos los resultados al final
resultados_incidencia = pd.concat(resultados_incidencia)

# Mostrar el DataFrame de resultados
print(resultados_incidencia)

# Guardamos archivo incidencia
ruta_incidencia='C:/Users/Elena/Desktop/TFG/mes 1/datos/incidencia_casos_suavizados.csv'
resultados_incidencia.to_csv(ruta_incidencia)

#Trazamos incidencia
plt.figure(figsize=(10,6))
plt.plot(resultados_incidencia.index, resultados_incidencia.incidencia, marker='o', linestyle='-', color='b' )
plt.title('Incidencia diaria')
plt.xlabel('Fecha')
plt.ylabel('Incidencia')
plt.grid(True)
plt.show()
#numero_filas=datos_csv_gripe.shape[0]
#print(f"El número de filas es: {numero_filas}")
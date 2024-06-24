# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:42:34 2024

@author: Elena
"""

import pandas as pd # data processing, CSV file


#Leemos el archivo CSV (dataframe datos diarios)
#ruta_archivo_dat_diar='C:/Users/Elena/Desktop/TFG/mes 1/datos/Vigil_ncia_sindr_mica_d_infeccions_a_Atenci__Prim_ria__Dades_di_ries__20240207.csv'
#dtype={'setmana_epidemiologica': 'int32', 'any': 'int32', 'codi_regio': 'int32', 'codi_ambit': 'int32', 'codi_abs': 'int32', 'index_socioeconomic': 'int32', 'casos': 'int32', 'poblacio': 'int32'}
#datos_diarios=pd.read_csv(ruta_archivo_dat_diar, dtype=dtype)
#Cogemos datos gripe
#filtro_datos_csv=datos_csv["diagnostic"] == "Grip"
#data_gripe=datos_diarios[datos_diarios["diagnostic"] == "Grip"]
#ruta archivo CSV (dataframe catsalut)

ruta_archivo_pob_ref='C:/Users/Elena/Desktop/TFG/mes 1/datos/Registre_central_de_poblaci__del_CatSalut__poblaci__per__rea_b_sica_de_salut_20240208.csv'
ruta_archivo_csv_gripe='C:/Users/Elena/Desktop/TFG/mes 1/datos/Vigil_ncia_sindr_mica_d_infeccions_a_Atenci__Prim_ria__Dades_di_ries__20240207_gripe.csv'

#leemos dataframe de la población de referencia
data_pob=pd.read_csv(ruta_archivo_pob_ref, dtype={'any': 'int32', 'Regió Sanitària': 'object'}, low_memory=False)

#leemos dataframe de datos diarios con gripe
data_gripe=pd.read_csv(ruta_archivo_csv_gripe)

#Definimos intervalos
intervalos=[0,2,4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79,float('inf')]
etiquetas=['0-2','3-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80 o más']

#Columna de rango de edad
data_pob['rango_edad']=pd.cut(data_pob['edat'], bins=intervalos, labels=etiquetas, right=False)

#Creamos archivo excel y un objeto excel workbook
archivo_excel='C:/Users/Elena/Desktop/TFG/mes 1/datos/Tabla_final.xlsx'

#abrimos archivo excel
with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a') as writer:

    #Iteramos sobre años y creamos tablas separadas
    for year, group_pob in data_pob.groupby('any'):
        tabla_anual_pob=group_pob.groupby('rango_edad')['població oficial'].sum().reset_index()
        
        #datos de la gripe para el mismo año
        group_gripe=data_gripe[data_gripe['any'] == year]
        
        # Diccionario de mapeo
        mapeo_intervalos = {
            '0': '0-2',
            '1 i 2': '0-2',
            '3 i 4': '3-4',
            '5 a 9': '5-9',
            '10 a 14': '10-14',
            '15 a 19': '15-19',
            '20 a 24': '20-24',
            '25 a 29': '25-29',
            '30 a 34': '30-34',
            '35 a 39': '35-39',
            '40 a 44': '40-44',
            '45 a 49': '45-49',
            '50 a 54': '50-54',
            '55 a 59': '55-59',
            '60 a 64': '60-64',
            '65 a 69': '65-69',
            '70 a 74': '70-74',
            '75 a 79': '75-79',
            '80 o más': '80 o más'
        }
        
        #'grup_edat' es una columna en el dataframe de datos diarios
        group_gripe['rango_edad'] = group_gripe['grup_edat'].map(mapeo_intervalos)
        
        #tabla de casos para cada año
        tabla_anual_casos=group_gripe.groupby('rango_edad')['casos'].sum().reset_index()
        
        #unimos las dos tablas
        tabla_final = pd.merge(tabla_anual_pob, tabla_anual_casos, on='rango_edad')
    
        nombre_hoja=f'Tabla_{year}'
        
        tabla_final.to_excel(writer, sheet_name=nombre_hoja, index=False)

    
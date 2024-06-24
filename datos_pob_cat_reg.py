# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:02:35 2024

@author: Elena
"""

import pandas as pd # data processing, CSV file

ruta_archivo_pob='C:/Users/Elena/Desktop/TFG/mes 1/datos/Registre_central_de_poblaci__del_CatSalut__poblaci__per__rea_b_sica_de_salut_20240208.csv'

#leemos dataframe de la población por área básica de salud
data_pob=pd.read_csv(ruta_archivo_pob, dtype={'any': 'int32', 'Regió Sanitària': 'object'}, low_memory=False)

#Creamos archivo excel 
archivo_excel='C:/Users/Elena/Desktop/TFG/mes 1/datos/Tabla_final_pob_cat_reg.xlsx'
df_vacio=pd.DataFrame()
df_vacio.to_excel(archivo_excel, index=False)

#abrimos archivo excel
with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a') as writer:

    #Iteramos sobre años y creamos tablas separadas
    for year, group_pob in data_pob.groupby('any'):
        
        tabla=group_pob.groupby(['Regió Sanitària','gènere'])['població oficial'].sum().reset_index()
        tabla_anual_pob=tabla.pivot(index='Regió Sanitària', columns='gènere', values='població oficial').reset_index()
        
        #Agregamos columna pob_total
        tabla_anual_pob['Total']=tabla_anual_pob['Dona']+tabla_anual_pob['Home']
        
        tabla_anual_pob = tabla_anual_pob[['Regió Sanitària', 'Home', 'Dona', 'Total']]
        
        tabla_anual_pob = tabla_anual_pob.rename(columns={'Home': 'Homes', 'Dona': 'Dones'})
        
        nombre_hoja=f'{year}'
        tabla_anual_pob.to_excel(writer, sheet_name=nombre_hoja, index=False)

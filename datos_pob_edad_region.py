# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:41:47 2024

@author: Elena
"""

import pandas as pd # data processing, CSV file

ruta_archivo_pob='C:/Users/Elena/Desktop/TFG/mes 1/datos/Registre_central_de_poblaci__del_CatSalut__poblaci__per__rea_b_sica_de_salut_20240208.csv'

#leemos dataframe de la población por área básica de salud
data_pob=pd.read_csv(ruta_archivo_pob, dtype={'any': 'int32', 'Regió Sanitària': 'object'}, low_memory=False)

recuento_edades = {}

# Calcular el recuento para cada edad en el rango deseado
for edad in range(86, 119):
    if edad in data_pob['edat'].unique():
        recuento = data_pob['edat'].value_counts()[edad]
    else:
        recuento = 0
    recuento_edades[edad] = recuento

# Imprimir los recuentos de cada edad
for edad, recuento in recuento_edades.items():
    print(f"Número de personas con {edad} años: {recuento}")
    
#Definimos intervalos
intervalos=[-1,0,2,4,9,14,44,59,69,79,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118]
etiquetas = ['0', '1 i 2', '3 i 4', '5 a 9', '10 a 14', '15 a 44', '45 a 59', '60 a 69', '70 a 79', '80 a 85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118']

data_pob['Edat']=pd.cut(data_pob['edat'], bins=intervalos, labels=etiquetas)

#Creamos archivo excel 
archivo_excel='C:/Users/Elena/Desktop/TFG/mes 1/datos/Tabla_final_pob_cat_reg_edad.xlsx'
df_vacio=pd.DataFrame()
df_vacio.to_excel(archivo_excel, index=False)
                  
#abrimos archivo excel
with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a') as writer:

    #Iteramos sobre años y creamos tablas separadas
    for year, group_pob in data_pob.groupby('any'):
        
        tabla=group_pob.groupby(['Edat','Regió Sanitària','gènere'])['població oficial'].sum().reset_index()
        tabla_anual_pob=tabla.pivot(index=['Regió Sanitària','Edat'], columns='gènere', values='població oficial').reset_index()
        
        #Agregamos columna pob_total
        tabla_anual_pob['Total']=tabla_anual_pob['Dona']+tabla_anual_pob['Home']
        
        tabla_anual_pob = tabla_anual_pob[['Regió Sanitària','Edat', 'Home', 'Dona', 'Total']]
        
        tabla_anual_pob = tabla_anual_pob.rename(columns={'Home': 'Homes', 'Dona': 'Dones'})
        
        # Insertamos una columna para la región sanitaria
        #tabla_anual_pob.insert(1, 'Regió Sanitària', tabla_anual_pob['Regió Sanitària'])
        nombre_hoja=f'{year}'
        tabla_anual_pob.to_excel(writer, sheet_name=nombre_hoja, index=False)

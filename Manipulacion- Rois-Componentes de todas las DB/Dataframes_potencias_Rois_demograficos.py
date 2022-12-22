"""
Code that allows to join the dataframes of all the evaluated databases, also joins them with 
the respective demographic data and neuropsychological tests, two dataframes of powers are obtained,
one by powers by columns of ROIs (for later use in a ML algorithm) and one with all the powers in a single column (for graphing).
"""

from cmath import nan
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display_html, display
import collections
from Funciones import dataframe_long_roi,ver_datos_vacios
from Funciones import columns_powers_rois

"Power data loading by ROIs"

path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD'

# SRM=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_powers_column_ROI_norm_SRM.feather'.format(path=path))
# CHBMP=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_powers_column_ROI_norm_CHBMP.feather'.format(path=path))
BIO=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_CE_power_columns_ROI_BIOMARCADORES.feather'.format(path=path))
DUQUE=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_resting_power_columns_ROI_DUQUE.feather'.format(path=path))

#datos=pd.concat([SRM,BIO,CHBMP,DUQUE]) #concatenation of data
datos=pd.concat([BIO,DUQUE]) #concatenation of data

datosICC=datos #Dataframe to work with

'''Loading of demographic data and neuropsychological tests from each database,
the necessary modifications are made to standardize the data in them'''

# #BIOMARCADORES
N_BIO=pd.read_excel('{path}\Datosparaorganizardataframes\Demograficosbiomarcadores.xlsx'.format(path=path))
N_BIO = N_BIO.rename(columns={'Codigo':'participant_id','Edad en la visita':'age','Sexo':'sex','Escolaridad':'education','MMSE':'MM_total','F':'FAS_F','S':'FAS_S','A':'FAS_A','Visita':'visit'})
N_BIO['participant_id']=N_BIO['participant_id'].replace({'_':''}, regex=True)# remove "_" and replace by "" in "participant_id"
N_BIO['participant_id']='sub-'+N_BIO['participant_id']
subjects_bio=N_BIO['participant_id'].unique()


for i in subjects_bio:
    num_vis=len(N_BIO[N_BIO['participant_id']==i].loc[:,'visit'])
    
    '''Since we do not have demographic and/or neuropsychological test data for all visits, 
    the values from the previous visit are assigned to the empty visits'''
    
    if num_vis==5:
        'Example to see how the data is before modifying'
        # print('Antes')
        # print(N_BIO[N_BIO['participant_id']==i])
        V0=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V0'
        V1=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V1'
        V2=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V2'
        V3=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V3'
        V4=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V4'
        index0=N_BIO[N_BIO['participant_id']==i].loc[V0].index.tolist()[0]
        index1=N_BIO[N_BIO['participant_id']==i].loc[V1].index.tolist()[0]
        index2=N_BIO[N_BIO['participant_id']==i].loc[V2].index.tolist()[0]
        index3=N_BIO[N_BIO['participant_id']==i].loc[V3].index.tolist()[0]
        index4=N_BIO[N_BIO['participant_id']==i].loc[V4].index.tolist()[0]
        #MM_total and FAS are modified
        if N_BIO[N_BIO['participant_id']==i].loc[V1]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index1,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index0,['MM_total','FAS_F','FAS_A','FAS_S']]
        if N_BIO[N_BIO['participant_id']==i].loc[V3]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index3,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index2,['MM_total','FAS_F','FAS_A','FAS_S']]
        if N_BIO[N_BIO['participant_id']==i].loc[V4]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index4,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index2,['MM_total','FAS_F','FAS_A','FAS_S']]
        'Example to see how the data is after modifying'
        # print('Despues')
        # print(N_BIO[N_BIO['participant_id']==i])

    if num_vis==4:
        V0=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V0'
        V1=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V1'
        V2=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V2'
        V3=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V3'
        index0=N_BIO[N_BIO['participant_id']==i].loc[V0].index.tolist()[0]
        index1=N_BIO[N_BIO['participant_id']==i].loc[V1].index.tolist()[0]
        index2=N_BIO[N_BIO['participant_id']==i].loc[V2].index.tolist()[0]
        index3=N_BIO[N_BIO['participant_id']==i].loc[V3].index.tolist()[0]
        #MM_total and FAS are modified
        if N_BIO[N_BIO['participant_id']==i].loc[V1]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index1,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index0,['MM_total','FAS_F','FAS_A','FAS_S']]
        if N_BIO[N_BIO['participant_id']==i].loc[V3]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index3,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index2,['MM_total','FAS_F','FAS_A','FAS_S']]    
        
    if num_vis==2:
        V0=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V0'
        V1=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V1'
        index0=N_BIO[N_BIO['participant_id']==i].loc[V0].index.tolist()[0]
        index1=N_BIO[N_BIO['participant_id']==i].loc[V1].index.tolist()[0]
        #MM_total and FAS are modified
        if N_BIO[N_BIO['participant_id']==i].loc[V1]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index1,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index0,['MM_total','FAS_F','FAS_A','FAS_S']]
        

# #CHBMP
# D_CHBMP=pd.read_csv("{path}\Datosparaorganizardataframes\Demographic_data_CHBMP.csv".format(path=path),header=1, sep=",")
# col_demC=['Code', 'Gender', 'Age',  'Education Level ']
# Dem_CHBMP=D_CHBMP.loc[:,col_demC]
# MMSE_CHBMP=pd.read_csv("{path}\Datosparaorganizardataframes\MMSE_CHBMP.csv".format(path=path),header=1)
# MMSE_CHBMP=MMSE_CHBMP.loc[:,['Code', 'Total Score']]
# N_CHBMP=pd.merge(left=Dem_CHBMP,right=MMSE_CHBMP, how='left', left_on='Code', right_on='Code')
# N_CHBMP = N_CHBMP.rename(columns={'Code':'participant_id','Age':'age','Gender':'sex','Education Level ':'education','Total Score':'MM_total'})
# N_CHBMP['participant_id']='sub-'+N_CHBMP['participant_id']

# #SRM
# N_SRM=pd.read_csv("{path}\Datosparaorganizardataframes\participantsSRM.tsv".format(path=path),sep='\t')
# N_SRM=N_SRM.loc[:,['participant_id', 'age', 'sex','vf_1','vf_2','vf_3']] #Elegí vf3 ya que tenia resultados mas parecidos a los de biomarcadores (habian 3 vf)
# N_SRM = N_SRM.rename(columns={'vf_1':'FAS_F','vf_2':'FAS_S','vf_3':'FAS_A'}) #Verificar con vero pero denom es igual a fluidez verbal?? creo que por eso la elegimos

#DUQUE
N_DUQUE=pd.read_csv('{path}\Datosparaorganizardataframes\demograficosDUQUE.csv'.format(path=path),sep=";")
N_DUQUE=N_DUQUE.loc[:,['participant_id','age','education','MM_total','group','sex']]
N_DUQUE['participant_id']=N_DUQUE['participant_id'].replace({'_':''}, regex=True)#Quito el _ y lo reemplazo con '' el participant Id
N_DUQUE['participant_id']='sub-'+N_DUQUE['participant_id']

#None is replaced by NaN
N_BIO.replace({'None':np.NaN},inplace=True)
# N_CHBMP.replace({'None':np.NaN},inplace=True)
# N_SRM.replace({'None':np.NaN},inplace=True)

'''The power data is merged with the demographic data, 
first merged for each database and then all the databases are concatenated.'''

# #SRM
# d_SRM=pd.merge(left=datosICC[datosICC['database']=='SRM'],right=N_SRM , how='left', left_on='participant_id', right_on='participant_id')
# #CHBMP
# d_CHBMP=pd.merge(datosICC[datosICC['database']=='CHBMP'],N_CHBMP)
# #BIOMARCADORES
d_BIO=pd.merge(datosICC[datosICC['database']=='BIOMARCADORES'],N_BIO)
#DUQUE
mergeDUQUE=datosICC[datosICC['database']=='DUQUE']
mergeDUQUE=mergeDUQUE.drop(['group'], axis=1)
d_DUQUE=pd.merge(mergeDUQUE,N_DUQUE)
#Data concatenation
#d_B=pd.concat([d_SRM,d_BIO,d_DUQUE,d_CHBMP])
d_B=pd.concat([d_BIO,d_DUQUE])
d_B['sex'].replace({'f':'F','m':'M','Masculino':'M','Femenino':'F'}, inplace=True) #Cambio a que queden con sexo F y M
d_B['education'].replace({'None':np.NaN,'University School':'17','High School':'12', 'Secondary School':'11','College School':'16',}, inplace=True)
d_B['education'] = d_B['education'].astype('float64')
#d_B['group'].replace({'CTR':'Control','G4':'Control','G3':'DTA'}, inplace=True)

'''Look at the amount of empty data in the databases before and after 
merging powers with demographic data and neuropsychological tests.'''

#Amount of empty data from the demographic data without joining with powers
df_dem=pd.DataFrame()
df_dem['BIOMARCADORES']=N_BIO.isnull().sum()
# df_dem['CHBMP']=N_CHBMP.isnull().sum()
# df_dem['SRM']=N_SRM.isnull().sum()
df_dem['DUQUE']=N_DUQUE.isnull().sum()

print('\nTotal de datos demograficos BIOMARCADORES',len(N_BIO))
# print('Total de datos demograficos CHBMP ',len(N_CHBMP))
# print('Total de datos demograficos SRM ',len(N_SRM))
print('Total de datos demograficos DUQUE ',len(N_DUQUE))



print('\nCantidad de datos vacios antes de unir el dataframe con los datos demograficos')
print(df_dem)
print('\nTotal de datos al unir los IC con datos demograficos')
ver_datos_vacios(d_B)

"Elimination of rows with empty data"
d_B.reset_index(inplace=True, drop=True)


#Rows are deleted per database
l=[]#list to store indexes that are not to be removed from the dataframe

'''With the dropna function, the database remains only with the data without empty data, 
and with the index function, it is possible to store the indexes without empty data in the list "l".'''

l.extend(d_B[d_B['database']=='BIOMARCADORES'].dropna(subset=['MM_total','FAS_F']).index.tolist())
# l.extend(d_B[d_B['database']=='SRM'].dropna(subset=['FAS_F']).index.tolist())
# l.extend(d_B[d_B['database']=='CHBMP'].dropna(subset=['MM_total','education']).index.tolist())
l.extend(d_B[d_B['database']=='DUQUE'].dropna(subset=['MM_total','education','age','sex']).index.tolist())

lista=list(set(l))
d_B=d_B.loc[lista,:]

print('\nCantidad de datos vacios luego de filtrar')
ver_datos_vacios(d_B)

d_B = d_B.sort_values('group')#Organized database
#Powers are saved in a feather file
d_B.reset_index().to_feather('{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas.feather'.format(path=path))

print('Dataframe de potencias de ROIs por columnas  y con datos demograficos guardado')

#d_B=d_B[d_B['database']=='DUQUE']

'''The dataframe is organized with all the powers in a single column to make the graphs in an easier way'''
dataframe_long_roi(d_B,'Power',columns=columns_powers_rois,name='Datos_ROI_formatolargo_filtrados',path=path)
print('Dataframe para hacer graficos de potencias por ROIs guardado ')

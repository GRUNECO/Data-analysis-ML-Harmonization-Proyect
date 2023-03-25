import collections
import pandas as pd 
import seaborn as sns
import numpy as np
import pingouin as pg
from numpy import ceil 
import errno
from matplotlib import pyplot as plt
import os
import io
from itertools import combinations
from PIL import Image
import matplotlib.pyplot as plt
import dataframe_image as dfi
import warnings
from Funciones import dataframe_long_roi,dataframe_long_components,dataframe_componentes_deseadas,dataframe_long_cross_ic,dataframe_long_cross_roi
from Funciones import columns_SL_roi,columns_coherence_roi,columns_entropy_rois,columns_powers_rois
#from Graficos_power_sl_coherencia_entropia_cross import graphics
warnings.filterwarnings("ignore")

path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes/' 
A = 'G2'
B = 'G1'
m = ['power','sl','cohfreq','entropy']
s = ['roi','ic']
#neuro = 'neuroHarmonize'
neuro = 'sovaharmony'
for space in s:
    #data_power=pd.read_feather(rf'{path}\Data_complete_{space}_{neuro}_{B+A}_power.feather')
    #data_sl=pd.read_feather(rf'{path}\Data_complete_{space}_{neuro}_{B+A}_sl.feather')
    #data_cohfreq=pd.read_feather(rf'{path}\Data_complete_{space}_{neuro}_{B+A}_cohfreq.feather')
    #data_entropy=pd.read_feather(rf'{path}\Data_complete_{space}_{neuro}_{B+A}_entropy.feather')
    #data_crossfreq=pd.read_feather(rf'{path}\Data_complete_{space}_{neuro}_{B+A}_crossfreq.feather')
    #data=pd.concat([data_power,data_sl,data_cohfreq,data_entropy,data_crossfreq], axis=1,)
    #data = data.T.drop_duplicates().T
    #new_name = 'Data_complete_'+space+'_'+neuro+'_'+A+B
    #data.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path,name=new_name))
    data_power=pd.read_feather(rf'{path}\Data_complete_{space}_neuroHarmonize_power.feather')
    data_sl=pd.read_feather(rf'{path}\Data_complete_{space}_neuroHarmonize_sl.feather')
    data_cohfreq=pd.read_feather(rf'{path}\Data_complete_{space}_neuroHarmonize_cohfreq.feather')
    data_entropy=pd.read_feather(rf'{path}\Data_complete_{space}_neuroHarmonize_entropy.feather')
    data_crossfreq=pd.read_feather(rf'{path}\Data_complete_{space}_neuroHarmonize_crossfreq.feather')
    data=pd.concat([data_power,data_sl,data_cohfreq,data_entropy,data_crossfreq], axis=1,)
    data = data.T.drop_duplicates().T
    new_name = 'Data_complete_'+space+'_neuroHarmonize'
    data.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path,name=new_name))
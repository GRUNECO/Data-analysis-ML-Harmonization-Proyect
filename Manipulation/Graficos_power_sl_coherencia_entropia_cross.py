
import collections
import pandas as pd 
import seaborn as sns
import numpy as np
#import pingouin as pg
from numpy import ceil 
import errno
from matplotlib import pyplot as plt
import os
import io
from itertools import combinations
from PIL import Image
import matplotlib.pyplot as plt
#import dataframe_image as dfi
from openpyxl import load_workbook
import warnings
warnings.filterwarnings("ignore")
import os
import tkinter as tk
from tkinter.filedialog import askdirectory


def graphics(data,type,path,name_band,id,id_cross=None,num_columns=2,save=True,plot=True,palette='winter_r'):
    '''Function to make graphs of the given data '''
    data['database'].replace({'BIOMARCADORES':'UdeA 1','DUQUE':'UdeA 2'}, inplace=True)
    max=data[type].max()
    min=data[type].min()
    prom=data[type].mean()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    if id=='IC':
        col='Component'
    else:
        col='ROI'
    #axs=sns.catplot(x='group',y=type,data=data,hue='database',dodge=True, kind="box",col=col,col_wrap=num_columns,palette=palette,fliersize=1.5,linewidth=0.5,legend=False)
    '''
    Modificación por correcciones del evaluador
    '''
    # Reemplazar 'G2' por control en la columna 'group'
    control='CTR'
    data['group'] = data['group'].replace('G2', control)
    axs=sns.catplot(x='group',y=type,data=data[data['group'] == control],hue='database',dodge=True, kind="box",col=col,col_wrap=num_columns,palette=palette,fliersize=1.5,linewidth=0.5,legend=False)
    '''
    Modificación por correcciones del evaluador
    '''
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.set_titles(size=20)
    if id=='IC':
        if band == 'Gamma' and metric == 'Cross Frequency' and bandm == 'Mgamma':
            # Set y-axis limit to 10 for each subplot
            axs.fig.suptitle(type+' in '+id_cross.replace('-','')+' of ' +r'$\bf{'+name_band.replace('-','')+r'}$'+ ' in the ICs of normalized data given by the databases',fontsize=20,x=0.55)
            for ax in axs.axes.flat:
                ax.set_ylim(0, 2.5)
                # Ajustar los límites del eje y en función del valor máximo del bigote
                #outliers = data[data['group'] == control][type].quantile(0.75) + 1.5 * (data[data['group'] == control][type].quantile(0.75) - data[data['group'] == control][type].quantile(0.25))
                #closest_outlier = data[data['group'] == control][type][abs(data[data['group'] == control][type] - outliers).idxmin()]
                #ax.set(ylim=(min - 0.10 , closest_outlier + 0.20))  # Agregar un margen de 10 unidades
                #ax.tick_params(axis='both', labelsize=20)
        elif id_cross==None:
            axs.fig.suptitle(type+' in '+r'$\bf{'+name_band.replace('-','')+r'}$'+ ' in the ICs of normalized data given by the databases',fontsize=20,x=0.55)
            if metric == 'Entropy' and band == 'Delta':
                print('Entropy')
                for ax in axs.axes.flat:
                    ax.set_ylim(0.40, 0.55)
            elif metric == 'SL' and band == 'Gamma':
                print('SL')
                for ax in axs.axes.flat:
                    ax.set_ylim(0.45, 0.58)
            else:
                # Obtener los valores de los bigotes y los límites
                for ax in axs.axes.flat:
                    # Ajustar los límites del eje y en función del valor máximo del bigote

                    outliers = data[data['group'] == control][type].quantile(0.75) + 1.5 * (data[data['group'] == control][type].quantile(0.75) - data[data['group'] == control][type].quantile(0.25))
                    closest_outlier = data[data['group'] == control][type][abs(data[data['group'] == control][type] - outliers).idxmin()]
                    ax.set(ylim=(min - 0.10, closest_outlier + 0.20))  # Agregar un margen de 10 unidades
                    ax.tick_params(axis='both', labelsize=20)
        else:
            axs.fig.suptitle(type+' in '+id_cross.replace('-','')+' of ' +r'$\bf{'+name_band.replace('-','')+r'}$'+ ' in the ICs of normalized data given by the databases',fontsize=20,x=0.55)
            # Obtener los valores de los bigotes y los límites
            for ax in axs.axes.flat:
                # Ajustar los límites del eje y en función del valor máximo del bigote
                outliers = data[data['group'] == control][type].quantile(0.75) + 1.5 * (data[data['group'] == control][type].quantile(0.75) - data[data['group'] == control][type].quantile(0.25))
                closest_outlier = data[data['group'] == control][type][abs(data[data['group'] == control][type] - outliers).idxmin()]
                ax.set(ylim=(min - 0.10, closest_outlier + 0.20))  # Agregar un margen de 10 unidades
                ax.tick_params(axis='both', labelsize=20)
        axs.add_legend(loc='upper right',bbox_to_anchor=(.8,.95),ncol=4,title="",fontsize=20)#title="Database"
        axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) 
        axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center',fontsize=30)
        axs.fig.text(0.01, 0.5,  type, ha='center', va='center',rotation='vertical',fontsize=30)


    else:
        if id_cross==None:
            axs.fig.suptitle(type+' in '+r'$\bf{'+name_band.replace('-','')+r'}$'+ ' in the ROIs of normalized data given by the databases',fontsize=20,x=0.55)
            # Obtener los valores de los bigotes y los límites
            for ax in axs.axes.flat:
                # Ajustar los límites del eje y en función del valor máximo del bigote
                outliers = data[data['group'] == control][type].quantile(0.75) + 1.5 * (data[data['group'] == control][type].quantile(0.75) - data[data['group'] == control][type].quantile(0.25))
                closest_outlier = data[data['group'] == control][type][abs(data[data['group'] == control][type] - outliers).idxmin()]
                ax.set(ylim=(min - 0.10, closest_outlier + 0.10))  # Agregar un margen de 10 unidades
                ax.tick_params(axis='both', labelsize=20)

        else:
            axs.fig.suptitle(type+' in '+id_cross.replace('-','')+' of ' +r'$\bf{'+name_band.replace('-','')+r'}$'+ ' in the ROIs of normalized data given by the databases',fontsize=20,x=0.55)
            # Obtener los valores de los bigotes y los límites
            for ax in axs.axes.flat:
                # Ajustar los límites del eje y en función del valor máximo del bigote
                outliers = data[data['group'] == control][type].quantile(0.75) + 1.5 * (data[data['group'] == control][type].quantile(0.75) - data[data['group'] == control][type].quantile(0.25))
                closest_outlier = data[data['group'] == control][type][abs(data[data['group'] == control][type] - outliers).idxmin()]
                ax.set(ylim=(min - 0.10, closest_outlier + 0.10))  # Agregar un margen de 10 unidades
                ax.tick_params(axis='both', labelsize=20)
        axs.add_legend(loc='upper right',bbox_to_anchor=(.8,.95),ncol=4,title="",fontsize=20)#title="Database"
        axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
        axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center',fontsize=30)
        axs.fig.text(0.015, 0.5,  type, ha='center', va='center',rotation='vertical',fontsize=30)


    if plot:
        plt.show()
    if save==True:
        verific = '{path}\Graficos_{type}\{id}'.format(path=path,name_band=name_band,id=id,type=type).replace('\\','/')
        if not os.path.exists(verific):
            os.makedirs(verific)  
        if id_cross==None:
            path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type).replace('\\','/')
            #path_complete= fr'C:\Users\veroh\OneDrive - Universidad de Antioquia\Verónica Henao Isaza\Resultados\graphics\unmatched\{name_band}_{type}_{id}.png'
        else:
            path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type,id_cross=id_cross).replace('\\','/')
            #path_complete= fr'C:\Users\veroh\OneDrive - Universidad de Antioquia\Verónica Henao Isaza\Resultados\graphics\unmatched\{name_band}_{id_cross}_{type}_{id}.png'
        plt.savefig(path_complete)
        plt.close()
        return path_complete
    else:
        return None
    


def text_format(val,value):
    if value==0.2: #Cambie el 0.05 por 0.2 y el lightgreen por lightblue
        color = 'lightblue' if val <0.2 else 'white'
    if value==0.7:
        color = 'lightgreen' if np.abs(val)>=0.7 else 'white'
    if value==0.0:
        color = 'lightblue' if np.abs(val)<=0.05 else 'white'
#    elif value==0.8:
#        if val >=0.7 and val<0.8:
#            color = 'salmon'
#        elif val >=0.8:
#            color = 'lightblue' 
#        else:
#            color='white'

    return 'background-color: %s' % color

def stats_pair(data,metric,space,path,name_band,id,id_cross=None):
    databases=data['database'].unique().tolist()
    for DB in databases:
        data_DB=data[data['database']==DB]
        groups=data_DB['group'].unique()
        if len(groups)==1:
            databases.remove(DB)
    tablas={}
    for DB in databases:
        data_DB=data[data['database']==DB]
        combinaciones=[('G2', 'G1'),('CTR','G1'),('CTR','G2'),('DCL','CTR'),('DCL','G1'),('DCL','G2'),('CTR','DCL')]
        test_ez={}
        test_std={}
        for i in combinaciones:
            #Effect size
            ez=data_DB.groupby(['database',space]).apply(lambda data_DB:pg.compute_effsize(data_DB[data_DB['group']==i[0]][metric],data_DB[data_DB['group']==i[1]][metric])).to_frame()
            ez=ez.rename(columns={0:'effect size'})
            ez['A']=i[0]
            ez['B']=i[1]
            ez['Prueba']='effect size'
            test_ez['effsize-'+i[0]+'-'+i[1]]=ez
            #cv
            std=data_DB.groupby(['database',space]).apply(lambda data_DB:np.std(np.concatenate((data_DB[data_DB['group']==i[0]][metric],data_DB[data_DB['group']==i[1]][metric]),axis=0))).to_frame()
            std=std.rename(columns={0:'cv'})
            std['A']=i[0]
            std['B']=i[1]
            std['Prueba']='cv'
            test_std['cv-'+i[0]+'-'+i[1]]=std
            
        table_ez=pd.concat(list(test_ez.values()),axis=0)
        table_ez.reset_index( level = [0,1],inplace=True )
        table_std=pd.concat(list(test_std.values()),axis=0)
        table_std.reset_index( level = [0,1],inplace=True )
        table_concat=pd.concat([table_ez,table_std],axis=0)
        table=pd.pivot_table(table_concat,values=['effect size','cv'],columns=['Prueba'],index=['database',space,'A', 'B'])
        tablas[DB]=table
        table.columns=['effect size','cv']
        tablas[DB]=table
    table=pd.concat(list(tablas.values()),axis=0)
    if id_cross==None:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}_table.png'.format(path=path,name_band=name_band,id=id,type=metric).replace('\\','/')
    else:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}_table.png'.format(path=path,name_band=name_band,id=id,type=metric,id_cross=id_cross).replace('\\','/')
    save_table = table.copy()
    table=table.style.applymap(text_format,value=0.7,subset=['effect size']).applymap(text_format,value=0.0,subset=['cv'])
    #dfi.export(table, path_complete)
    return path_complete,save_table

def create_check(table,space,name_band,metric,state,mband=None):
    if state == 'different':
        #check = table[(np.abs(table['effect size']) > 0.5) & (np.abs(table['cv']) < 0.1)] 
        check = table[(np.abs(table['effect size']) > 0.5)] 
    else:
        check = table[(np.abs(table['effect size']) <= 0.5) & (np.abs(table['cv']) < 0.1)]
        #check = table[(np.abs(table['effect size']) <= 0.5)]
    check['space'] = space
    check['state'] = state
    check['band'] = name_band
    #check['mband'] = mband
    check['metric'] = metric
    check = check.reset_index()
    return check

def std_poolsd(x,y):
    nx, ny = x.size, y.size
    dof = nx + ny - 2
    poolsd = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / dof)
    d = (x.mean() - y.mean()) / poolsd
    return d

def table_groups_DB(data,metric,space,path,name_band,id,id_cross=None):
    data=data[data['group']!='DCL'].copy()
    groups=data['group'].unique().tolist()
    tablas={}
    for g in groups:
        data_g=data[data['group']==g]
        databases=data_g['database'].unique()
        combinaciones = list(combinations(databases, 2))
        test_ez={}
        test_std={}
        for i in combinaciones:
            #Effect size
            ez=data_g.groupby(['group',space]).apply(lambda data_g:pg.compute_effsize(data_g[data_g['database']==i[0]][metric],data_g[data_g['database']==i[1]][metric])).to_frame()
            ez=ez.rename(columns={0:'effect size'})
            ez['A']=i[0]
            ez['B']=i[1]
            ez['Prueba']='effect size'
            test_ez['effsize-'+i[0]+'-'+i[1]]=ez
            #cv
            std=data_g.groupby(['group',space]).apply(lambda data_g:np.std(np.concatenate((data_g[data_g['database']==i[0]][metric],data_g[data_g['database']==i[1]][metric]),axis=0))).to_frame()
            std=std.rename(columns={0:'cv'})
            std['A']=i[0]
            std['B']=i[1]
            std['Prueba']='cv'
            test_std['cv-'+i[0]+'-'+i[1]]=std
        table_ez=pd.concat(list(test_ez.values()),axis=0)
        table_ez.reset_index( level = [0],inplace=True )
        table_std=pd.concat(list(test_std.values()),axis=0)
        table_std.reset_index( level = [0],inplace=True )
        table_concat=pd.concat([table_ez,table_std],axis=0)
        table=pd.pivot_table(table_concat,values=['effect size','cv'],columns=['Prueba'],index=['group',space,'A', 'B'])
        # table=table.T
        # table=table.swaplevel(0, 1)
        # table.sort_index(level=0,inplace=True)
        # table=table.T
        tablas[g]=table
        table.columns=['effect size','cv']
        tablas[g]=table
    table=pd.concat(list(tablas.values()),axis=0)
    if id_cross==None:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}_table_DB.png'.format(path=path,name_band=name_band,id=id,type=metric)  
    else:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}_table_DB.png'.format(path=path,name_band=name_band,id=id,type=metric,id_cross=id_cross)
    save_table = table.copy()
    table=table.style.applymap(text_format,value=0.7,subset=['effect size']).applymap(text_format,value=0.0,subset=['cv'])
    #dfi.export(table, path_complete)
    return path_complete,save_table

def joinimages(paths):
    import sys
    from PIL import Image
    images =[Image.open(x) for x in paths]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    new_im.save(paths[1])
    print('Done!')

#path=r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD' #Cambia dependieron de quien lo corra
path=r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_Correcciones_Evaluador\Datosparaorganizardataframes\11092023\sovaharmony\long G1' #Cambia dependieron de quien lo corra
#path=r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_Correcciones_Evaluador' #Cambia dependieron de quien lo corra
#path=r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_54x10' #Cambia dependieron de quien lo corra
#path = askdirectory() 
path='/media/gruneco-server/ADATA HD650/BIOMARCADORES/derivatives/data_columns/IC'

#data loading
#data_p_roi=pd.read_feather(fr'{path}\data_long_power_roi_without_oitliers.feather')
#data_p_com=pd.read_feather(fr'{path}\data_long_power_components_without_oitliers.feather')
#data_sl_roi=pd.read_feather(fr'{path}\data_long_sl_roi.feather')
#data_sl_com=pd.read_feather(fr'{path}\data_long_sl_components.feather')
#data_c_roi=pd.read_feather(fr'{path}\data_long_coherence_roi.feather')
#data_c_com=pd.read_feather(fr'{path}\data_long_coherence_components.feather')
#data_e_roi=pd.read_feather(fr'{path}\data_long_entropy_roi.feather')
#data_e_com=pd.read_feather(fr'{path}\data_long_entropy_components.feather')
#data_cr_roi=pd.read_feather(fr'{path}\data_long_crossfreq_roi.feather')
#data_cr_com=pd.read_feather(fr'{path}\data_long_crossfreq_components.feather')

#data loading sovaharmony
data_p_roi=pd.read_feather(fr'{path}\data_long_power_roi_without_oitliers.feather')
data_p_com=pd.read_feather(fr'{path}\data_long_power_components_without_oitliers.feather')
data_sl_roi=pd.read_feather(fr'{path}\data_long_sl_roi.feather')
data_sl_com=pd.read_feather(fr'{path}\data_long_sl_ic.feather')
data_c_roi=pd.read_feather(fr'{path}\data_long_coherence_roi.feather')
data_c_com=pd.read_feather(fr'{path}\data_long_coherence_ic.feather')
data_e_roi=pd.read_feather(fr'{path}\data_long_entropy_roi.feather')
data_e_com=pd.read_feather(fr'{path}\data_long_entropy_ic.feather')
data_cr_roi=pd.read_feather(fr'{path}\data_long_crossfreq_roi.feather')
data_cr_com=pd.read_feather(fr'{path}\data_long_crossfreq_ic.feather')

#datos_roi={'Power':data_p_roi,'SL':data_sl_roi,'Coherence':data_c_roi,'Entropy':data_e_roi,'Cross Frequency':data_cr_roi}
#datos_com={'Power':data_p_com,'SL':data_sl_com,'Coherence':data_c_com,'Entropy':data_e_com,'Cross Frequency':data_cr_com}
datos_roi={'Cross Frequency':data_cr_roi}
datos_com={'Cross Frequency':data_cr_com}
#data_p_roi=pd.read_feather(fr'{path}\Datosparaorganizardataframes\revisar\data_long_power_roi_without_oitliers.feather')
#data_p_com=pd.read_feather(fr'{path}\Datosparaorganizardataframes\data_long_power_components_without_oitliers.feather')
data_p_com=pd.read_feather(fr'{path}\data_BIOMARCADORES_CE_columns_irasa_54x10_components.feather'.replace('\\','/'))
#data_sl_roi=pd.read_feather(fr'{path}\Datosparaorganizardataframes\data_long_sl_roi.feather')
#data_sl_com=pd.read_feather(fr'{path}\Datosparaorganizardataframes\data_long_sl_components.feather')
#data_c_roi=pd.read_feather(fr'{path}\Datosparaorganizardataframes\revisar\data_long_coherence_roi.feather')
#data_c_com=pd.read_feather(fr'{path}\Datosparaorganizardataframes\data_long_coherence_components.feather')
#data_e_roi=pd.read_feather(fr'{path}\Datosparaorganizardataframes\revisar\data_long_entropy_roi.feather')
#data_e_com=pd.read_feather(fr'{path}\Datosparaorganizardataframes\data_long_entropy_components.feather')
#data_cr_roi=pd.read_feather(fr'{path}\Datosparaorganizardataframes\revisar\data_long_crossfreq_roi.feather')
#data_cr_com=pd.read_feather(fr'{path}\Datosparaorganizardataframes\data_long_crossfreq_components.feather')+-

#datos_roi={'Power':data_p_roi,'SL':data_sl_roi,'Coherence':data_c_roi,'Entropy':data_e_roi,'Cross Frequency':data_cr_roi}
#datos_com={'Power':data_p_com,'SL':data_sl_com,'Coherence':data_c_com,'Entropy':data_e_com,'Cross Frequency':data_cr_com}
#datos_roi={'SL':data_sl_roi}
datos_com={'power':data_p_com}
bands= data_p_com['Band'].unique()
bandsm= data_p_com['M_Band'].unique()

bands= data_p_com['Band'].unique()
#bandsm= data_p_com['M_Band'].unique()
#matrix_roi=pd.DataFrame(columns=['group', 'ROI', 'A', 'B', 'cv', 'effect size', 'space', 'state','band','mband', 'metric'])
matrix_com=pd.DataFrame(columns=['group', 'Component', 'A', 'B', 'cv', 'effect size', 'space', 'state','band','mband', 'metric'])

palette = ["#8AA6A3","#127369","#10403B","#45C4B0"]

for metric in datos_com.keys():
    for band in bands:
        d_roi=datos_com[metric]
        d_banda_roi=d_roi[d_roi['Band']==band]
        d_com=datos_com[metric]
        d_banda_com=d_com[d_com['Band']==band]
        if metric!='Cross Frequency':  
            print(str(band)+' '+str(metric)) 
            #table_roi,save_roi=stats_pair(d_banda_roi,metric,'ROI',path,band,'ROI')
            #check_roi=create_check(save_roi,'ROI',band,metric,'different',None)
            table_com,save_com=stats_pair(d_banda_com,metric,'Component',path,band,'IC') 
            check_com=create_check(save_com,'Component',band,metric,'different',None)
            #path_roi=graphics(d_banda_roi,metric,path,band,'ROI',num_columns=2,save=True,plot=False,palette=palette)
            path_com=graphics(d_banda_com,metric,path,band,'IC',num_columns=2,save=True,plot=False,palette=palette)
            #tg_roi,save_tg_roi=table_groups_DB(d_banda_roi,metric,'ROI',path,band,'ROI',id_cross=None)
            #check_tg_roi=create_check(save_tg_roi,'ROI',band,metric,'equal',None)
            tg_com,save_tg_com=table_groups_DB(d_banda_com,metric,'Component',path,band,'IC',id_cross=None)
            #check_tg_com=create_check(save_tg_com,'Component',band,metric,'equal',None)
            #joinimages([path_roi,table_roi,tg_roi])
            joinimages([path_com,table_com,tg_com])
            # os.remove(tg_roi)
            # os.remove(tg_com)
            #matrix_roi = matrix_roi.append(check_roi, ignore_index = True)
            #matrix_com = matrix_com.append(check_com, ignore_index = True)
            #matrix_roi = matrix_roi.append(check_tg_roi, ignore_index = True)
            matrix_com = matrix_com.append(check_tg_com, ignore_index = True)
            
        else:
            for bandm in bandsm:  
                print(str(band)+' '+str(metric)+' '+str(bandm)) 
                if d_banda_roi[d_banda_roi['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
                    #table_roi,save_roi=stats_pair(d_banda_roi[d_banda_roi['M_Band']==bandm],metric,'ROI',path,band,'ROI',id_cross=bandm)
                    #check_roi=create_check(save_roi,'ROI',band,metric,'different',bandm)
                    #path_roi=graphics(d_banda_roi[d_banda_roi['M_Band']==bandm],'Cross Frequency',path,band,'ROI',id_cross=bandm,num_columns=2,save=True,plot=False,palette=palette)
                    #tg_roi,save_tg_roi=table_groups_DB(d_banda_roi[d_banda_roi['M_Band']==bandm],metric,'ROI',path,band,'ROI',id_cross=bandm)
                    #check_tg_roi=create_check(save_tg_roi,'ROI',band,metric,'equal',bandm)
                    # joinimages([path_roi,table_roi,tg_roi])    
                    # os.remove(tg_roi)
                    #matrix_roi = matrix_roi.append(check_roi, ignore_index = True)
                    #matrix_roi = matrix_roi.append(check_tg_roi, ignore_index = True)
                    pass
                
                try:
                    if d_banda_com[d_banda_com['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
                        table_com,save_com=stats_pair(d_banda_com[d_banda_com['M_Band']==bandm],metric,'Component',path,band,'IC',id_cross=bandm) 
                        check_com=create_check(save_com,'Component',band,metric,'different',bandm)
                        path_com=graphics(d_banda_com[d_banda_com['M_Band']==bandm],'Cross Frequency',path,band,'IC',id_cross=bandm,num_columns=2,save=True,plot=False,palette=palette)
                        tg_com,save_tg_com=table_groups_DB(d_banda_com[d_banda_com['M_Band']==bandm],metric,'Component',path,band,'IC',id_cross=bandm)
                        check_tg_com=create_check(save_tg_com,'Component',band,metric,'equal',bandm)
                        # joinimages([path_com,table_com,tg_com])
                        # os.remove(tg_com) 
                        #matrix_com = matrix_com.append(check_com, ignore_index = True)
                        matrix_com = matrix_com.append(check_tg_com, ignore_index = True)   
                except:
                    pass

            matrix_com = pd.concat((matrix_com,check_com), ignore_index = True)
            #matrix_roi = matrix_roi.append(check_tg_roi, ignore_index = True)
            #matrix_com = matrix_com.append(check_tg_com, ignore_index = True)
        #     for bandm in bandsm:  
        #         print(str(band)+' '+str(metric)+' '+str(bandm)) 
        #         if d_banda_roi[d_banda_roi['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
        #             #table_roi,save_roi=stats_pair(d_banda_roi[d_banda_roi['M_Band']==bandm],metric,'ROI',path,band,'ROI',id_cross=bandm)
        #             #check_roi=create_check(save_roi,'ROI',band,metric,'different',bandm)
        #             #path_roi=graphics(d_banda_roi[d_banda_roi['M_Band']==bandm],'Cross Frequency',path,band,'ROI',id_cross=bandm,num_columns=2,save=True,plot=False,palette=palette)
        #             #tg_roi,save_tg_roi=table_groups_DB(d_banda_roi[d_banda_roi['M_Band']==bandm],metric,'ROI',path,band,'ROI',id_cross=bandm)
        #             #check_tg_roi=create_check(save_tg_roi,'ROI',band,metric,'equal',bandm)
        #             # joinimages([path_roi,table_roi,tg_roi])    
        #             # os.remove(tg_roi)
        #             #matrix_roi = matrix_roi.append(check_roi, ignore_index = True)
        #             #matrix_roi = matrix_roi.append(check_tg_roi, ignore_index = True)
        #             pass
                
        #         if d_banda_com[d_banda_com['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
        #             table_com,save_com=stats_pair(d_banda_com[d_banda_com['M_Band']==bandm],metric,'Component',path,band,'IC',id_cross=bandm) 
        #             check_com=create_check(save_com,'Component',band,metric,'different',bandm)
        #             path_com=graphics(d_banda_com[d_banda_com['M_Band']==bandm],'Cross Frequency',path,band,'IC',id_cross=bandm,num_columns=2,save=True,plot=False,palette=palette)
        #             tg_com,save_tg_com=table_groups_DB(d_banda_com[d_banda_com['M_Band']==bandm],metric,'Component',path,band,'IC',id_cross=bandm)
        #             check_tg_com=create_check(save_tg_com,'Component',band,metric,'equal',bandm)
        #             # joinimages([path_com,table_com,tg_com])
        #             # os.remove(tg_com) 
        #             matrix_com = matrix_com.append(check_com, ignore_index = True)
        #             matrix_com = matrix_com.append(check_tg_com, ignore_index = True)   

print('table lista')
matrix_com['Compared groups']=matrix_com['A']+'-'+matrix_com['B']
#matrix_roi['Compared groups']=matrix_roi['A']+'-'+matrix_roi['B']
filename = r"{path}\power_54x10_different.xlsx".format(path=path).replace('\\','/')
writer = pd.ExcelWriter(filename)
matrix_com.to_excel(writer ,sheet_name='Component')
#matrix_roi.to_excel(writer ,sheet_name='ROI')
writer._save()
writer.close()              
print('Graficos SL,coherencia,entropia y cross frequency guardados')
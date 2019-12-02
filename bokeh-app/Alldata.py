# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:38:48 2019

@author: yary0
"""
from os.path import join, dirname
import numpy as np
import pandas as pd

months=['april','may','june','july','august','september','october','november']

files=['data\tipificacion_'+m +'.xlsx' for m in months]
dfs=[]
for f in files:
    
    data=pd.ExcelFile(join(dirname(__file__), f))
    df=data.parse('atento')
    dfs.append(df)

df=pd.concat(dfs, axis=0, ignore_index=True)    
    
df.drop(columns='Provider',axis=1,inplace=True) 

df['ws_date']=pd.to_datetime(df['ws_date'],format='%Y/%m/%d') 

dfbydate=df.groupby(['ws_date','sub_description']).count()

dfbydate.rename(columns={'id_movistar':'Count'},inplace=True)


dfbymonth=dfbydate.groupby(by=[pd.Grouper(level=0, freq='M'), pd.Grouper(level=1)])['Count'].sum()

dfbymonth=dfbymonth.reset_index()


dfbymonth.rename(columns={'ws_date':'month'},inplace=True)

dfbymonth.sort_values(by=['month','Count'], ascending=[True,True], inplace=True)

dfbymonth['month']=dfbymonth.month.map(lambda x : x.month)


description=list(np.sort(dfbymonth.sub_description.unique()))

desc_ids=list(np.asarray([1,1,1,2,3,4,5,6,7,7,8,9,9,2,2,10,11,12,12,13,14,15,15,16,17,18,19,20,
         21,22,23,24,25,26,26,27,28,29,30,31,32,33,34,35,35,36,37,38,39,40,40,40,
          41,40,40])-1)

dict_desc={k:v  for k, v in zip(description,desc_ids)}

dfbymonth['ids']=dfbymonth.sub_description.map(dict_desc)

aux=pd.DataFrame(data={'description':description,'ids':desc_ids})

aux=aux.groupby('ids')['description'].first().reset_index()

dfbymonth=pd.merge(left=dfbymonth,right=aux, on='ids', how='left')

dfbymonth.drop(columns=['sub_description','ids'],axis=1,inplace=True)

dfbymonth.rename(columns={'description': 'sub_description'},inplace=True)

dfbymonth=dfbymonth.groupby(['month','sub_description']).Count.sum().reset_index()

description=dfbymonth.sort_values(by='Count').sub_description.unique()

dfbydate.reset_index(inplace=True)

dfbydate['ids']=dfbydate.sub_description.map(dict_desc)

dfbydate=pd.merge(left=dfbydate, right= aux, on='ids', how='left')

dfbydate.drop(columns=['sub_description','ids'],axis=1,inplace=True)
dfbydate.rename(columns={'description':'sub_description'},inplace=True)
dfbydate=dfbydate.groupby(['ws_date','sub_description']).Count.sum().reset_index()
dfbydate.set_index('ws_date',inplace=True)








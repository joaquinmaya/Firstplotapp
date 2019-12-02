import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from bokeh.io import output_file, show,curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import widgetbox,row
from bokeh.models import Slider
from bokeh.models.annotations import Title
import Alldata

dfbymonth=Alldata.dfbymonth
description=Alldata.description
dfbydate=Alldata.dfbydate


source=ColumnDataSource(data={'x':dfbymonth[dfbymonth.month==4].Count,
                              'description':dfbymonth[dfbymonth.month==4].sub_description})

hover=HoverTool(tooltips=[('Count','@x')])

p=figure(y_range=description, x_axis_label='Count', 
         y_axis_label='description', plot_height=700, x_range=(0,2000))

p.hbar(right='x', y='description', height=0.2 ,source=source)

p.add_tools(hover)

menu= Select(title='Frequency',options=['day','month'],value='month')

slider=Slider(title='month',start=4, end=11, step=1, value=4)

def update_time(attr,old,new):
    time=slider.value
    if menu.value=='month':
        new_data={'x':dfbymonth[dfbymonth.month==time].Count,
              'description':dfbymonth[dfbymonth.month==time].sub_description}
    if menu.value=='day':
        new_data={'x':dfbydate[dfbydate.index.dayofyear==time].Count,
                  'description':dfbydate[dfbydate.index.dayofyear==time].sub_description}
        
    source.data=new_data



   

def update_freq(attr,old,new):
    freq=menu.value
    if freq=='day':
        p.x_range.end=300
        slider.title='day'
        slider.start=dfbydate.index.dayofyear.min()
        slider.end=dfbydate.index.dayofyear.max()
        slider.value=dfbydate.index.dayofyear.min()
        new_data={'x':dfbydate[dfbydate.index.dayofyear==slider.value].Count,
                  'description':dfbydate[dfbydate.index.dayofyear==slider.value].sub_description}
        
    if freq=='month':       
        p.x_range.end=2000
        slider.title='month'
        slider.start=dfbymonth.month.min()
        slider.end=dfbymonth.month.max()
        slider.value=dfbymonth.month.min()
        new_data={'x':dfbymonth[dfbymonth.month==slider.value].Count,
              'description':dfbymonth[dfbymonth.month==slider.value].sub_description}
    
    source.data=new_data    
    



menu.on_change('value',update_freq)
slider.on_change('value',update_time)
         
    

layout=row(widgetbox([menu,slider]),p)


curdoc().add_root(layout)

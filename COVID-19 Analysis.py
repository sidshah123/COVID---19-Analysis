#!/usr/bin/env python
# coding: utf-8

# In[4]:


from __future__ import print_function
import numpy as np 
import pandas as pd 
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


# In[5]:


df_country = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
df_death = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')


# In[6]:


df_death.head()


# In[7]:


df_recovered.head()


# In[8]:


df_confirmed.head()


# In[9]:


df_country.head()


# In[10]:


df_recovered.columns = map(str.lower, df_recovered.columns)
df_confirmed.columns = map(str.lower, df_confirmed.columns)
df_death.columns = map(str.lower, df_death.columns)
df_country.columns = map(str.lower, df_country.columns)


# In[11]:


df_confirmed = df_confirmed.rename(columns = {'province/state' : 'state', 'country/region' : 'country'})
df_recovered = df_confirmed.rename(columns = {'province/state' : 'state', 'country/region' : 'country'})
df_death = df_death.rename(columns = {'province/state' : 'state', 'country/region' : 'country'})
df_country = df_country.rename(columns = {'country_region' : 'country' })


# In[12]:


sorted_df_country = df_country.sort_values('confirmed' , ascending=False).head(20)
sorted_df_country


# In[13]:


def highlight_col(x):
    r = 'background-color: red'
    p = 'background-color: purple'
    g = 'background-color: green'
    temp_df = pd.DataFrame('', index=x.index , columns = x.columns)
    temp_df.iloc[:,4] = p 
    temp_df.iloc[:,5] = r
    temp_df.iloc[:,6] = g
    return temp_df
sorted_df_country.style.apply(highlight_col, axis=None)
    
    
        


# In[14]:


df_country = df_country.rename(columns = {'country_region' : 'country' })
df_country.head()


# In[15]:


import plotly.express as px


# In[16]:


fig = px.scatter(sorted_df_country.head(10), x ='country' , y ='confirmed', size ='confirmed', color ='country', hover_name = 'country', size_max = 60)
fig.show()


# In[17]:


import plotly.graph_objects as go
def plot_cases_for_country(country):
    labels = ['confirmed', 'death']
    colors = ['blue','red']
    mode_size = [6,8]
    line_size = [4,5]
    df_list = [df_confirmed, df_death]
    fig = go.Figure()
    for i , df in enumerate (df_list):
        if country == 'World' or country == 'world':
            x_data = np.array(list(df.iloc[:,5:].columns))
            y_data = np.sum(np.asarray(df.iloc[:,5:]),axis=0)
        
        else:
            x_data = np.array(list(df.iloc[:,5:].columns))
            y_data = np.sum(np.asarray(df[df['country']==country].iloc[:,5:]), axis=0)
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode= 'lines+markers',name=labels[i],line = dict(color=colors[i],width=line_size[i]),connectgaps=True,text = "Total"+ str(labels[i])+ ": "+ str(y_data[-1])))
    fig.show()
        

interact(plot_cases_for_country, country = 'World')


# In[106]:


import folium


# In[110]:


world_map = folium.Map(location=[11,0], tiles="cartodbpositron", zoom_start=2 , max_zoom= 6, min_zoom=2)
for i in range(len(df_confirmed)):
    folium.Circle(
    location=[df_confirmed.iloc[i]['lat'], df_confirmed.iloc[i]['long']],
    fill = True,
    radius = (int((np.log(df_confirmed.iloc[i,-1]+1.00001)))+0.2)*50000,
    fill_color = 'blue',
    color = 'red',
    tooltip =  "<div style='margin: 0; background-color: black; color: white;'>"+
                    "<h4 style='text-align:center;font-weight: bold'>"+df_confirmed.iloc[i]['country'] + "</h4"
                    "<hr style='margin:10px;color: white;'>"+
                    "<ul style= 'color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                    "<li>Confirmed: "+str(df_confirmed.iloc[i,-1])+"<li>"+
                    "<li>Deaths:"+str(df_death.iloc[i,-1])+"<li>"+
                    "<li>Death rate: "+str(np.round(df_death.iloc[i,-1]/(df_confirmed.iloc[i,-1]+1.00001)*100,2))+ "</li>"+
                    "</ul></div>",

    ).add_to(world_map)
world_map
          


# In[ ]:





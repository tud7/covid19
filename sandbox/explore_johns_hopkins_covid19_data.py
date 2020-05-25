#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Explore the COVID-19 data from Johns Hopkins

Coronavirus Disease 2019 (COVID-19) is a disease that was first identified in Wuhan, China, 
and later spread throughout the world

Author: Tu Duong

Copyright © 2020 Tu Duong All Rights Reserved
'''

import os
import csv
import glob
import urllib
import urllib.request
import urllib.error
import matplotlib.pyplot    as plt
import ipywidgets           as widgets
import pandas               as pd
import numpy                as np
import plotly.graph_objects as go
import plotly.express       as px


# In[2]:


def get_latest_report():
    
    current_dir  = os.path.dirname(os.path.realpath('__file__'))
    jh_daily_dir = os.path.join(current_dir, 'johns_hopkins_data',                                 'csse_covid_19_data', 'csse_covid_19_daily_reports')
    
    pat           = os.path.join(jh_daily_dir, '*.csv')
    csv_files     = glob.glob(pat)
    latest_report = sorted(csv_files, reverse=True)[0] 
    
    return 'file://%s' %latest_report


# In[3]:


def load_data(url=None):
    '''
    Function to download latest data from the WHO URL and load into the data frame
    '''
    
    if url is None:
        url = get_latest_report()
        print(url)
        
    try:
        df = pd.read_csv(url)
        
    except urllib.error.HTTPError as ex:
        print('WARNING: Unable to retrieve data...')
        print(' - INFO:', ex)
        
    return df


# In[4]:


df = load_data()

condition = df['Country_Region']=='US'
data      = df[condition]

total_confirmed = data['Confirmed'].sum()
total_deaths    = data['Deaths'].sum()
total_recovered = data['Recovered'].sum()
total_unknown   = total_confirmed - (total_deaths + total_recovered)

labels_map = {'Unknown'  :'lightgrey',
              'Recovered':'green',
              'Deaths'   :'darkred'}

labels = list( labels_map.keys() ) # get list of labels
values = [total_unknown, total_recovered, total_deaths]

fig = px.pie(df, values=values, names=labels, 
             title='COVID-19 United States Statistics', 
             color=labels,
             color_discrete_map=labels_map)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()


# In[ ]:





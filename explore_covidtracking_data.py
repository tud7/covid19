#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Explore the COVID-19 data from www.covidtracking.com

Coronavirus Disease 2019 (COVID-19) is a disease that was first identified in Wuhan, China, 
and later spread throughout the world

Author: Tu Duong

Copyright © 2020 Tu Duong All Rights Reserved
'''

import os
import csv
import glob
import datetime
import urllib
import urllib.request
import urllib.error
import matplotlib.pyplot    as plt
import ipywidgets           as widgets
import pandas               as pd
import numpy                as np
import plotly.graph_objects as go
import plotly.express       as px

from plotly.subplots import make_subplots


# In[2]:


def load_tests_data():
    
    url='https://covidtracking.com/api/v1/us/daily.csv'

    df = pd.read_csv(url)
    df = df.sort_values(by='date', ascending=True)

    df.date = [datetime.datetime.strptime(str(d), '%Y%m%d').strftime("%b-%d") for d in df.date]
    
    return df


# In[3]:


def load_sp500_data():
    
    current_dir  = os.path.dirname(os.path.realpath('__file__'))
    jh_daily_dir = os.path.join(current_dir, 'GSPC.csv')

    df = pd.read_csv(jh_daily_dir)
    df = df.sort_values(by='Date', ascending=True)

    df.Date = [datetime.datetime.strptime(d, '%Y-%m-%d').strftime("%b-%d") for d in df.Date]

    return df


# In[4]:


testdata_df  = load_tests_data()
sp500data_df = load_sp500_data()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(name='S&P 500',
                     x=sp500data_df.Date,
                     y=sp500data_df.Close,
                     marker_color='orange',
                     connectgaps=True),
             secondary_y=True)

fig.add_trace(go.Bar(name='Cumulative Tests', 
                     x=sp500data_df.Date, 
                     y=testdata_df.totalTestResults, 
                     marker_color='blue', 
                     opacity=0.4),
             secondary_y=False)

fig.add_trace(go.Bar(name='Daily Tests',
                     x=sp500data_df.Date,
                     y=testdata_df.totalTestResultsIncrease,
                     marker_color='darkblue'),
             secondary_y=False)

fig.update_layout(
    title='COVID-19 (Cumulative and Daily) Tests vs. S&P 500',
    barmode='overlay',
    bargap=0.3,    # gap between bars of adjacent location coordinates
)

fig.update_yaxes(title_text="Number of Tests (Millions)", secondary_y=False)
fig.update_yaxes(title_text="S&P 500 Index", secondary_y=True)

fig.show()


# In[ ]:





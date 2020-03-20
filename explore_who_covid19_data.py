#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Explore the COVID-19 data

Coronavirus Disease 2019 (COVID-19) is a disease that was first identified in Wuhan, China, 
and later spread throughout the world

The dataset is retrieved from World Health Organization (WHO) Situation Reports which includes:
date  location  new_cases  new_deaths  total_cases  total_deaths

Author: Tu Duong

Copyright © 2020 Tu Duong All Rights Reserved
'''

import csv
import urllib
import urllib.request
import urllib.error
import matplotlib.pyplot as plt
import ipywidgets        as widgets
import pandas            as pd


# In[2]:


cases_vs_deaths_out = widgets.Output()
new_cases_out       = widgets.Output()


# In[3]:


def load_data(url, archived_csv=None):
    '''
    Function to download latest data from the WHO URL and load into the data frame
    '''
    
    try:
        df = pd.read_csv(url)
        
        #TODO: archive csv file if successfully read for offline use
        
    except urllib.error.HTTPError as ex:
        print('WARNING: Unable to retrieve data...')
        print(' - INFO:', ex)
        
        if archived_csv is not None:
            df = pd.read_csv(archived_csv)
            print(' - INFO: Loading the archived data: ', archived_csv)

    return df


# In[4]:


def plot_data(selected_location, yxs, output_widget, title=''):
    '''
    Function to plot data based on the selected location
    '''
    with output_widget:
        
        output_widget.clear_output(wait=True)
        
        filter_condition  = df['location']==selected_location
        _data        = df[filter_condition]

        plt.figure(figsize=(10,5))
        ax = plt.gca()

        plt.title(title)
        
        for y in yxs:
            _data.plot(kind='line', x='date', y=y,  ax=ax)

        plt.grid()
        plt.show()


# In[5]:


def on_location_change(change):
    '''
    Function will be called when user select the new value in the dropdown list
    '''
    
    selected_location = change.new
    plot_data(selected_location, ['total_cases', 'total_deaths'], cases_vs_deaths_out, "Covid-19 Total Cases vs. Total Deaths")
    

def on_location_change2(change):
    '''
    Function will be called when user select the new value in the dropdown list
    '''
    
    selected_location = change.new
    plot_data(selected_location, ['new_cases'], new_cases_out, "Covid-19 Day-by-Day New Cases")


# In[6]:


# load data into pandas data frame
covid19_fulldata_url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
df = load_data(url=covid19_fulldata_url, archived_csv="who_covid19_data_20200317.csv")


# In[7]:


default_location = "World"

# the dropdown list allows user to select the location
location_dropdown = widgets.Dropdown(
    options=df.location.unique(),
    value=default_location,
    description='Location:',
    disabled=False,
)
location_dropdown.observe(on_location_change, names='value')

plot_data(default_location, ['total_cases', 'total_deaths'], cases_vs_deaths_out, "Covid-19 Total Cases vs. Total Deaths")
display(location_dropdown)
display(cases_vs_deaths_out)


# In[8]:


default_location2 = "World"

# the dropdown list allows user to select the location
location_dropdown2 = widgets.Dropdown(
    options=df.location.unique(),
    value=default_location,
    description='Location:',
    disabled=False,
)
location_dropdown2.observe(on_location_change2, names='value')

plot_data(default_location, ['new_cases'], new_cases_out, "Covid-19 Day-by-Day New Cases")
display(location_dropdown2)
display(new_cases_out)


# In[ ]:





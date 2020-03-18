#!/usr/bin/env python
# coding: utf-8

# In[95]:


'''
Explore the COVID-19 data

Coronavirus Disease 2019 (COVID-19) is a disease that was first identified in Wuhan, China, 
and later spread throughout the world

The dataset is retrieved from World Health Organization (WHO) Situation Reports which includes:
date  location  new_cases  new_deaths  total_cases

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


# In[96]:


def load_data():
    '''
    Function to download latest data from the WHO URL and load into the data frame
    '''
    
    csv_file = 'latest_who_covid19_data.csv'
    try:
        
        url = 'https://covid.ourworldindata.org/data/full_data.csv'
        urllib.request.urlretrieve(url, csv_file)
        
    except urllib.error.HTTPError as ex:
        print('WARNING: Unable to retrieve data...')
        print(' - INFO:', ex)
        
        csv_file = 'who_covid19_data_20200317.csv'
        print(' - INFO: Loading the default data: ', csv_file)

    # read data into pandas data frame
    df = pd.read_csv(csv_file)

    return df


# In[97]:


output_widget = widgets.Output()
    
def plot_data(selected_location):
    '''
    Function to plot data based on the selected location
    '''
    with output_widget:
        
        output_widget.clear_output(wait=True)
        
        filter_condition  = df['location']==selected_location
        _data        = df[filter_condition]

        plt.figure(figsize=(12,6))
        ax = plt.gca()

        plt.title("Covid-19 Total Cases vs. Total Deaths")
        
        _data.plot(kind='line', x='date', y='total_cases',  ax=ax)
        _data.plot(kind='line', x='date', y='total_deaths', ax=ax)

        plt.grid()
        plt.show()


# In[98]:


def on_location_change(change):
    '''
    Function will be called when user select the new value in the dropdown list
    '''
    
    selected_location = change.new
    plot_data(selected_location)


# In[99]:


# load data into pandas data frame
df = load_data()

default_location = "World"

# the dropdown list allows user to select the location
location_dropdown = widgets.Dropdown(
    options=df.location.unique(),
    value=default_location,
    description='Location:',
    disabled=False,
)
location_dropdown.observe(on_location_change, names='value')

plot_data(default_location)
display(location_dropdown)
display(output_widget)


# In[ ]:





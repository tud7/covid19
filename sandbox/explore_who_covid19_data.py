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

import os
import csv
import urllib
import urllib.request
import urllib.error
import matplotlib.pyplot as plt
import ipywidgets        as widgets
import pandas            as pd


# In[2]:


def load_data(url, archived_csv='latest_fulldata_archived.csv'):
    """Function to load data from the URL into the pandas data frame
    
    Keyword arguments:
    url          -- URL to read the data from
    archived_csv -- [optional] path to the archive file in case we can't read 
                    the data from the provided URL
    """
    
    try:
        df = pd.read_csv(url)
        
        # Archive to csv file after successfully read for future offline use
        df.to_csv(archived_csv)
        
    except urllib.error.HTTPError as ex:
        print('WARNING: Unable to retrieve data...')
        print(' - INFO:', ex)
        
        if os.path.exists(archived_csv):
            df = pd.read_csv(archived_csv)
            print(' - INFO: Loading the archived data: ', archived_csv)

    return df


# In[3]:


def plot_data(selected_location, yxs, output_widget, title='', kind='line'):
    """ Function to plot data based on the provided arguments
    
    Keyword arguments:
    selected_location -- the selected location
    yxs               -- list of all interested data to include in this plot
    output_widget     -- the output widget to display the plot
    title             -- optional title of the plot
    kind              -- plot kind, default to 'line'
    """
    with output_widget:
        
        output_widget.clear_output(wait=True)
        
        filter_condition  = df['location']==selected_location
        _data        = df[filter_condition]

        plt.figure(figsize=(10,5))
        ax = plt.gca()

        plt.title(title)
        
        for y in yxs:
            _data.plot(kind=kind, x='date', y=y,  ax=ax)

        plt.grid()
        plt.show()


# In[4]:


def on_location_change1(change):
    '''
    Function will be called when user select the new value in the dropdown list #1
    '''
    
    selected_location = change.new
    plot_data(selected_location, ['total_cases', 'total_deaths'], cases_vs_deaths_out, title="Covid-19 Total Cases vs. Total Deaths")
    

def on_location_change2(change):
    '''
    Function will be called when user select the new value in the dropdown list #2
    '''
    
    selected_location = change.new
    plot_data(selected_location, ['new_cases'], new_cases_out, title="Covid-19 Day-by-Day New Cases", kind="bar")


# In[5]:


# load data into pandas data frame
covid19_fulldata_url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
df = load_data(url=covid19_fulldata_url)

cases_vs_deaths_out = widgets.Output()
new_cases_out       = widgets.Output()
default_location    = "United States"


# In[6]:




# Plot Total Cases vs Total Deaths

# the dropdown list allows user to select the location
location_dropdown1 = widgets.Dropdown(
    options=df.location.unique(),
    value=default_location,
    description='Location:',
    disabled=False,
)
# Set the callback function when the value changed.
location_dropdown1.observe(on_location_change1, names='value')

plot_data(default_location, ['total_cases', 'total_deaths'], cases_vs_deaths_out, "Covid-19 Total Cases vs. Total Deaths")
display(location_dropdown1)
display(cases_vs_deaths_out)


# In[7]:


# Plot Daily New Cases

# the dropdown list allows user to select the location
location_dropdown2 = widgets.Dropdown(
    options=df.location.unique(),
    value=default_location,
    description='Location:',
    disabled=False,
)
location_dropdown2.observe(on_location_change2, names='value')

plot_data(default_location, ['new_cases'], new_cases_out, title="Covid-19 Day-by-Day New Cases", kind='bar')
display(location_dropdown2)
display(new_cases_out)


# In[ ]:





import os
import glob
import subprocess
import urllib
import urllib.request
import urllib.error

import pandas as pd
from abc import ABC, abstractmethod


class DataSource(ABC):

    def __init__(self, url):
        
        self.url = url
        self._read_data()
        self._reformat_data()
        self._unify_date()
        
     
    def _read_data(self):
        '''Read data from the url into the panda dataframe'''
        
        try:
            self.df = pd.read_csv(self.url)
        
        except urllib.error.HTTPError as ex:
            print('WARNING: Unable to retrieve data...')
            print(' - INFO:', ex)
    
    
    def _unify_date(self):
        '''Unify 'date' column to the same data type for easy merging and plotting'''
        
        try:
            self.df['date'] = pd.to_datetime(self.df['date'])
        except:
            pass
    
    
    def get_full_data(self):
        '''Function to get full data frame'''
        
        return self.df
    
    
    def _reformat_data(self):
        pass
    
    
    @abstractmethod
    def get_US_data(self):
        '''Funtion to return United States data'''
        pass
        
        
class JohnHopkins(DataSource):

    def __init__(self, url=None):
        super().__init__(self._get_latest_JH_report())
        
    
    def get_US_data(self):
        return self.df[ self.df['Country_Region']=='US' ]
    
    
    def _get_latest_JH_report(self):
        
        self._update_submodule()

        current_dir  = os.path.dirname(os.path.realpath('__file__'))
        jh_daily_dir = os.path.join(current_dir, 'johns_hopkins_data', \
                                'csse_covid_19_data', 'csse_covid_19_daily_reports')
    
        pat           = os.path.join(jh_daily_dir, '*.csv')
        csv_files     = glob.glob(pat)
        latest_report = sorted(csv_files, reverse=True)[0]
    
        return 'file://%s' %latest_report
    
    
    def _update_submodule(self):
        subprocess.run(['git', 'submodule', 'update', '--remote'], capture_output=True)


class CovidTracking(DataSource):
    
    def __init__(self):
        super().__init__('https://covidtracking.com/api/v1/us/daily.csv')
    
    
    def _reformat_data(self):
        
        self.df = self.df.sort_values(by='date', ascending=True)
        
        # convert to string first since 'date' column is int64.
        # to_datetime() function won't work well with int64
        self.df['date'] = self.df['date'].astype(str)
        
    
    def get_US_data(self):
        return self.df
        
        
class OurWorldInData(DataSource):
    
    def __init__(self):
        super().__init__('https://covid.ourworldindata.org/data/ecdc/full_data.csv')
    
    
    def get_US_data(self):
        return self.df[ self.df['location']=='United States' ]


        
    
    
    
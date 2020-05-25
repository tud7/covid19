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
        self.read_data()
        self._reformat_data()
        
     
    def read_data(self):
        '''Read data from the url into the panda dataframe'''
        
        try:
            self.df = pd.read_csv(self.url)
            self._reformat_data()
        
        except urllib.error.HTTPError as ex:
            print('WARNING: Unable to retrieve data...')
            print(' - INFO:', ex)
    
    
    @abstractmethod
    def _reformat_data(self):
        pass
    
    
    def get_full_data(self):
        '''Function to get full data frame'''
        return self.df
        
        
class JohnHopkins(DataSource):

    def __init__(self, url):
        
        if url is None:
            url = self._get_latest_JH_report()
            
        super().__init__(url)
        
    
    def _reformat_data(self):
        pass
    
    
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
    
    def __init__(self, url):
        super().__init__(url)
    
    
    def _reformat_data(self):
        
        self.df = self.df.sort_values(by='date', ascending=True)
        
        # convert 'date' column to the same data type for merging later
        # note: we need to convert to string first since us_covid19_test_data['date'] is int64.
        # to_datetime won't work well with int64
        self.df['date'] = self.df['date'].astype(str) 
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        
class OurWorldInData(DataSource):
    
    def __init__(self, url):
        super().__init__(url)
    
    
    def _reformat_data(self): 
        self.df['date'] = pd.to_datetime(self.df['date'])
        


        
    
    
    
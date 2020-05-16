import os
import glob
import urllib
import urllib.request
import urllib.error

import pandas as pd
from abc import ABC, abstractmethod


class DataSource(ABC):

    def __init__(self, url):
        
        self.url = url
        self.df  = self.read_data()
        
     
    def read_data(self):
        '''Read data from the url into the panda dataframe'''
        
        try:
            df = pd.read_csv(self.url)
            df = self._reformat_data(df)
        
        except urllib.error.HTTPError as ex:
            print('WARNING: Unable to retrieve data...')
            print(' - INFO:', ex)
            
        return df
        
    @abstractmethod
    def _reformat_data(self, df):
        pass
        
        
class JohnHopkins(DataSource):

    def _reformat_data(self, df):
        pass


url = 'file://05-15-2020.csv'
print(url)
x = JohnHopkins(url)
        
    
    
    
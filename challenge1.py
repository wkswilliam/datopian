#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:47:31 2020

@author: william
"""
import os
import pandas as pd
import argparse
import json
import traceback

parser = argparse.ArgumentParser(
    description="Collect US Gas Price in Different Granularities"
    )
parser.add_argument('-g', '--granularity', type=str, default='d',
                    choices=['d','w','m','a'], required=True,
                    help="You must choose a valid granularity. \n"+
                             "Example: 'd' for daily, " +
                             "'w' for weekly, " +
                             "'m' for monthly or " + 
                             "'a' for annual.")
args = parser.parse_args()

class DataCollector():
    labels = {'d':'Daily',
              'w':'Weekly',
              'm':'Monthly',
              'a':'Annual'}
    def __init__(self, granularity="d"):
        self.name = f"{self.labels[granularity]} Prices of US Natural Gas"
        self.path = f"data/gas_price_us_{granularity}.csv"
        self.author = "William Kramer Scariot"
        self.title =  f"{self.labels[granularity]} US Natural Gas Price"
        self.profile = "Tabular Data Package"
        self.description = f"{self.labels[granularity]} prices of natural gas in the US since 1997."
        self.keywords = "Gas Price, US, Historical prices of gas"
        self.granularity = granularity
        
    def fetch_and_process(self):
        """
        Fetch the US gas price history for a given granularity.
        
        Returns
        -------
        df : pandas.DataFrame
            US gas prices formated.

        """
        try:
            df = pd.read_excel(f"https://www.eia.gov/dnav/ng/hist_xls/RNGWHHD{self.granularity}.xls",
                               sheet_name=1,
                               skiprows=2)
            df.columns = ['Date', 'Price']
        except Exception:
            traceback.print_exc()
        return df
            
    def store(self):
        """
        Store the US gas prices in csv format and update the datapackage.json file.
        """
        try:
            if os.path.isfile('./datapackage.json'):
                with open('datapackage.json') as json_file:
                    datapackage = json.load(json_file)
            else:
                datapackage = {"profile": "tabular-data-package",
                               "resources": []}
            for old in datapackage.get('resources', []):
                if self.name == old.get('name', ''):
                    datapackage['resources'].remove(old)
            new = dict(self.__dict__)
            new.pop('granularity')
            new['schema'] = {"fields": [{"name": "Date",
                                         "type": "text",
                                         "format": "default",
                                         "title": "Date"},
                                        {"name": "Price",
                                         "type": "integer",
                                         "format": "default",
                                         "title": "Price"}]}
            datapackage['resources'].append(new)
            with open('datapackage.json', 'w') as fp:
                json.dump(datapackage, fp, sort_keys=True, indent=4)
            df = self.fetch_and_process()
            df.to_csv(f'data/gas_price_us_{self.granularity}.csv', index=False)
        except Exception:
            traceback.print_exc()
        return None
    

def main(granularity):
    dc = DataCollector(granularity=granularity)
    dc.store()
    
    
if __name__=="__main__":
    main(args.granularity)
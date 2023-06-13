#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:16:54 2023

@author: user
"""

import pandas as pd
from itertools import chain

class DataProcessor:
    
    def __init__(self, config, data):
        self.data = data
        self.config = config
        
    def extract_data_for_study(self):
        # the retrieved data are in a json, here we retrieve the needed data
        # print(self.data)
        all_data = sum([data[self.config.data_name] for data in self.data], [])
        # data is a list of dictionnary and we just want to retrieve "values"
        needed_data = [value[self.config.values] for value in all_data]
        # the needed data is a list of list of dictionnary, we just want a 
        # list of dictionnary so that we can transform it into a pandas
        # dataFrame
        flattened_list = list(chain(*needed_data))
        return pd.DataFrame(flattened_list)
    
    def compute_hour_to_hour_mean(self):
        data = self.extract_data_for_study()
        pivot_column = self.config.pivot_column
        # get hour of the day
        data[pivot_column] = data[pivot_column].apply(lambda date: pd.to_datetime(date).hour)
        # we compute the mean and sum of electricity production as asked
        hour_to_hour_mean = data.groupby(pivot_column)[self.config.value].agg(["mean","sum"]).reset_index()
        # change the column names so that it is clearer
        hour_to_hour_mean.columns = [pivot_column, "average_daily_production", "sum_of_daily_production"]
        return hour_to_hour_mean
    
    def data_to_json(self, df):
        data = df[[self.config.pivot_column,"sum_of_daily_production"]]
        data = data.to_dict(orient='records')
        return data
    
        
        
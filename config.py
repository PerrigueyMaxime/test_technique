#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:24:08 2023

@author: user
"""

import yaml

class Config:
    
    def __init__(self, path):
        # read yaml file which contains all needed informations
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        # get information and put them in variables
        self.authorization_url = self.config.get("authorization_url") 
        self.api_url = self.config.get("api_url") 
        self.content_type = self.config.get("content_type")
        self.authorization = self.config.get("authorization")

        self.start_date = self.config.get("start_date")
        self.end_date = self.config.get("end_date")
        self.max_chunk = self.config.get("max_chunk")
        self.data_name = self.config.get("data_name")
        self.value = self.config.get("value")
        self.values = self.config.get("values")
        self.pivot_column = self.config.get("pivot_column")

    def get(self, key):
        keys = key.split('.')
        val = self.config
        for key in keys:
            value = val.get(key)
            if value is None:
                return None
        return value
    
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:01:25 2023

@author: user
"""

import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import pytz


class DataRetriever:
    
    def __init__(self, config):
        self.config = config
        
    def create_authorization_headers(self):
        # create header so that we can get the access token
        return {
            'content-type': self.config.content_type,
            'Authorization': self.config.authorization,
        }
    
    def get_access_token(self):
        headers = self.create_authorization_headers()
        # call the url with needed params to get access_token
        response = requests.post(self.config.authorization_url, headers=headers)
        authorization_code = response.content
        # retrieve access_token
        access_token = json.loads(authorization_code.decode('utf-8'))["access_token"]
        return access_token

    def period_into_subsets(self, start_date, end_date, max_chunk):
        periods = []
    
        current_date = start_date
        while current_date < end_date:
            period_end_date = current_date + timedelta(days=max_chunk)
            if period_end_date > end_date:
                period_end_date = end_date
            periods.append((current_date, period_end_date))
            current_date += timedelta(days=max_chunk)
        return periods
    
    @staticmethod
    def get_timezone(date):
        france_tz = pytz.timezone('Europe/Paris')
        # Obtention du décalage horaire à partir de la date spécifique
        offset = france_tz.utcoffset(date)
        return int(offset.seconds/3600)
    
    def build_url(self, start_date, end_date):
        print(f"start_date: {start_date}, end_date: {end_date}")
        utc_offset = DataRetriever.get_timezone(start_date)
        offset_for_date = f"%2B0{utc_offset}:00"
        start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S') + offset_for_date
        end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S') + offset_for_date
        url = self.config.api_url + f"?start_date={start_date}&end_date={end_date}"
        return url
    
    def get_data_api(self, start_date, end_date, max_chunk):
        access_token = self.get_access_token()
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        print(start_date, end_date)
        periods = self.period_into_subsets(start_date, end_date, max_chunk)
        data = [
            requests.get(self.build_url(date[0], date[1]), headers=headers)
            .json() 
            for date in periods]
        return data

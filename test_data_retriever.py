#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 20:16:11 2023

@author: user
"""

from datetime import datetime
import unittest

from config import Config
from data_retriever import DataRetriever

config_path = "/Users/user/Documents/test_technique/config/config_file.yaml"  

class TestDataRetriever(unittest.TestCase):
    
    def setUp(self):
        # Initialize test data
        self.config = Config(config_path)
        self.data_retriever = DataRetriever(self.config)

    def test_create_authorization_headers(self):
        data_retriever = DataRetriever(self.config)
        headers = data_retriever.create_authorization_headers()
        self.assertEqual(headers['content-type'], 'application/x-www-form-urlencoded')
        self.assertEqual(headers['Authorization'], 'Basic your_client_and_secret_id_in_64')

    def test_period_into_subsets(self):
        data_retriever = DataRetriever(self.config)
        periods = data_retriever.period_into_subsets(max_chunk=5)
        expected_periods = [
            (datetime(2022, 12, 1, 0, 0), datetime(2022, 12, 6, 0, 0)),
            (datetime(2022, 12, 6, 0, 0), datetime(2022, 12, 11, 0, 0)),
            (datetime(2022, 12, 11, 0, 0), datetime(2022, 12, 11, 0, 0))
        ]
        self.assertEqual(periods, expected_periods)

    def test_get_timezone(self):
        date = datetime(2023, 1, 1, 12, 0, 0)
        data_retriever = DataRetriever({})
        timezone = data_retriever.get_timezone(date)
        self.assertEqual(timezone, 1)  # UTC+1 for France
    
    def test_build_url(self):
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        end_date = datetime(2023, 1, 5, 0, 0, 0)
        url = self.data_retriever.build_url(start_date, end_date)
        expected_url = 'https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit?start_date=2023-01-01T00:00:00%2B01:00&end_date=2023-01-05T00:00:00%2B01:00'
        self.assertEqual(url, expected_url)
    

if __name__ == '__main__':
    unittest.main()
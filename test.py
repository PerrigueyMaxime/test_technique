#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 16:20:27 2023

@author: user
"""
    

import unittest
import pandas as pd
from itertools import chain
from data_processor import DataProcessor
from config import Config

config_path = "config/config_file.yaml"  

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        # Initialize test data
        self.config = Config(config_path)
        
        self.data = [
            {
                "actual_generations_per_unit": [
                    {
                        "values": [
                            {"start_date": "2022-01-01", "value": 10},
                            {"start_date": "2022-01-02", "value": 15}
                        ]
                    }
                ]
            },
            {
                "actual_generations_per_unit": [
                    {
                        "values": [
                            {"start_date": "2022-01-01", "value": 20},
                            {"start_date": "2022-01-02", "value": 25}
                        ]
                    }
                ]
            }
        ]
        self.data_processor = DataProcessor(self.config, self.data)

    def test_extract_data_for_study(self):
        expected_result = pd.DataFrame([
            {"start_date": "2022-01-01", "value": 10},
            {"start_date": "2022-01-02", "value": 15},
            {"start_date": "2022-01-01", "value": 20},
            {"start_date": "2022-01-02", "value": 25}
        ])
        result = self.data_processor.extract_data_for_study()
        pd.testing.assert_frame_equal(result, expected_result)

    
    def test_compute_hour_to_hour_mean(self):
        expected_result = pd.DataFrame([
            {"start_date": 0, "average_daily_production": 17.5, "sum_of_daily_production": 70}
        ])
        result = self.data_processor.compute_hour_to_hour_mean()
        pd.testing.assert_frame_equal(result, expected_result)

    
    def test_data_to_json(self):
        expected_result = [
            {"start_date": 0, "sum_of_daily_production": 70}
        ]
        df = self.data_processor.compute_hour_to_hour_mean()
        result = self.data_processor.data_to_json(df)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

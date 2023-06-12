#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:01:48 2023

@author: user
"""


  
from flask import Flask, render_template, jsonify
from config import Config
from data_processor import DataProcessor
from data_retriever import DataRetriever

MAX_CHUNK = 7

class MyApp(Flask):
    config = None
    
    def __init__(self, config_path, *args, **kwargs):
        MyApp.config = Config(config_path)
        super().__init__(*args, **kwargs)

    @classmethod
    def index(cls):
        # retrieve data from API
        retrieved_data = DataRetriever(cls.config).get_data_api(MAX_CHUNK)
        # get hour to hour mean and sum
        data_processor = DataProcessor(cls.config, retrieved_data)
        processed_data = data_processor.compute_hour_to_hour_mean()
        data = data_processor.data_to_json(processed_data)
        return render_template('rendu_js.html',data=data)

# path for the yaml config file
config_path = "/Users/user/Documents/etude_de_cas_edf/config/config_file.yaml"    
app = MyApp(config_path, __name__)
app.route('/')(MyApp.index)

if __name__ == '__main__':
    app.run(debug=True)
    

#il faut que je fasse un bouton dans le html qui lance une fonction en javascript.
# une fonction en python qui va regénérer la data.
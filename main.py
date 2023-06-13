#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:01:48 2023

@author: user
"""


  
from flask import Flask, render_template, redirect, session, jsonify, url_for
import schedule
import time
import random
from datetime import datetime, timedelta

from config import Config
from data_processor import DataProcessor
from data_retriever import DataRetriever

MAX_CHUNCK = 7
start_date = datetime(2020,1,1,0,0,0)


class MyApp(Flask):
    config = None
    app_instance = None
    
    def __init__(self, config_path, *args, **kwargs):
        MyApp.config = Config(config_path)
        super().__init__(*args, **kwargs)
        MyApp.app_instance = self
    
    @staticmethod
    def set_title(start_date, end_date):
        return f"Somme de la production infrajournalière de toute les centrales du {start_date} au {end_date}"
    
    def render(start_date, end_date):
        retrieved_data = DataRetriever(MyApp.config).get_data_api(start_date, end_date, MAX_CHUNCK)
        # Traiter les données
        data_processor = DataProcessor(MyApp.config, retrieved_data)
        processed_data = data_processor.compute_hour_to_hour_mean()
        data = data_processor.data_to_json(processed_data)
        # Mettre à jour les données dans la session
        response = {
        'reload': True,
        'data': data,
        'title': MyApp.set_title(start_date, end_date)
        }
        #session['response'] = response
        # Rediriger vers la page rendu_js.html pour mettre à jour le rendu
        return render_template('rendu_js.html', response=response, start_date=start_date)
        
    def bonus():
        global start_date
        start_date += timedelta(days=1)
        end_date = start_date + timedelta(days=MAX_CHUNCK)
        # Récupérer les nouvelles données
        return MyApp.render(start_date, end_date)
    
    def cas_de_base():
        start_date, end_date = datetime(2022,12,1,0,0,0), datetime(2022,12,11,0,0,0)
        return MyApp.render(start_date, end_date)
        
    """
    @classmethod
    def index(cls):
        with cls.app_instance.test_request_context('/'):
            print("-------index-------")
            response = {
            'reload': False,
            'data': []
            }
            session["response"] = response
            return MyApp.update_data_and_render()
    """
    

# path for the yaml config file
config_path = "config/config_file.yaml"    
app = MyApp(config_path, __name__)


@app.route('/cas_de_base')
def cas_de_base():
    return MyApp.cas_de_base()

@app.route('/bonus')
def bonus():
    return MyApp.bonus()

@app.route('/read_start_date')
def read_start_date():
    global start_date
    return jsonify(start_date)

if __name__ == '__main__':
    random.seed()

    # Planifiez la mise à jour des données toutes les heures
    
    schedule.every(10).seconds.do(bonus)
    print("schedule every 10 seconds")
    # Fonction pour exécuter la planification
    def run_schedule():
        while True:
            with app.app_context():
                schedule.run_pending()
            time.sleep(1)

    # Exécutez l'application Flask dans un thread séparé
    import threading
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()

    # Exécutez la planification dans le thread principal
    run_schedule()
    
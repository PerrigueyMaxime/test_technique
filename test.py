#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 16:20:27 2023

@author: user
"""
    

import unittest
from flask import Flask, render_template
from main import MyApp

class MyAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = MyApp('/Users/user/Documents/etude_de_cas_edf/config/config_file.yaml', __name__)

    def tearDown(self):
        pass

    def test_index_route(self):
        with self.app.test_client() as client:
            response = client.get('/')
            print(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'text/html; charset=utf-8')
            self.assertIsInstance(response.data, bytes)
            self.assertIn(b'<title>MyApp</title>', response.data)

    def test_index_render_template(self):
        with self.app.app_context():
            rendered_template = render_template('rendu_js.html', data=...)
            self.assertIsNotNone(rendered_template)
            # Effectuez d'autres vérifications sur le contenu de la template si nécessaire

if __name__ == '__main__':
    unittest.main()

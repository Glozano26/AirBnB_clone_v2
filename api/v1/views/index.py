#!/usr/bin/python3
"""
Contains the app_views
"""
from flask import jsonify
from api.v1.views import app_views

# app_views = Flask(__name__)


@app_views.route('/status')
def status():
    """"functions that return JSON"""
    data = {'status': 'OK'}
    return jsonify(data)

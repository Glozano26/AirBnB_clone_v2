#!/usr/bin/python3
"""
Contains the app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

# app_views = Flask(__name__)


@app_views.route('/status')
def status():
    """"functions that return JSON"""
    data = {'status': 'OK'}
    return jsonify(data)


@app_views.route('/api/v1/stats')
def counts():
    """Create an endpoint that retrieves the number of each objects by type"""
    num_objs = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("States"),
        "users": storage.count("Users")
    }
    return jsonify(num_objs)

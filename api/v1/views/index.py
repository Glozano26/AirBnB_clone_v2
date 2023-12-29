#!/usr/bin/python3
"""
Contains the app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """"functions that return JSON"""
    data = {'status': 'OK'}
    return jsonify(data)


@app_views.route('/stats')
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

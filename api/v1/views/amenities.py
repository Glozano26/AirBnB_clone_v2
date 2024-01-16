#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = storage.all(Amenity)
    list_amenity = [amenitis.dict() for amenitis in all_amenities.values()]
    return jsonify(list_amenity)


# @app_views.route('/amenities/<amenity_id>', methods=['GET'])
# def get_amenity(amenity_id):
#     """Retrieves a Amenity object"""
#     try:
#         return jsonify(storage.get(Amenity, amenity_id).to_dict())
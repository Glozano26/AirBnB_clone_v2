#!/usr/bin/python3
"""Same as State, create a new view for City objects that handles
all default RESTFul API actions:"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_from_a_state(state_id):
    '''Get all the cities from a state'''
    state = storage.get(State, state_id)
    if state is None:
        return {'error': 'Not found'}, 404
    list_of_cities = []
    cities = storage.all(City)
    for city in cities.values():
        if city.state_id == state_id:
            list_of_cities.append(city.to_dict())
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_a_city(city_id):
    '''Get one specific city'''
    city = storage.get(City, city_id)
    if city is None:
        return {'error': 'Not found'}, 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Delete one city'''
    city = storage.get(City, city_id)
    if city is None:
        return {'error': 'Not found'}, 404
    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_new_city(state_id):
    '''Create a new city'''
    state = storage.get(State, state_id)
    if state is None:
        return {'error': 'Not found'}, 404
    if request.is_json:
        data = request.get_json()
        if "name" in data:
            new_city_data = dict(data, **{"state_id": state_id})
            new_city = City(**new_city_data)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        return {'error': 'Missing name'}, 400
    return {'error': 'Not a JSON'}, 400


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        return {'error': 'Not found'}, 404

    cities_HTTP = request.get_json()

    if cities_HTTP is None:
        return jsonify({'error': 'Not a JSON'}), 400

    keys_ignored = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in cities_HTTP.items():
        if key not in keys_ignored:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

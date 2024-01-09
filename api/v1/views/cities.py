#!/usr/bin/python3
"""Same as State, create a new view for City objects that handles
all default RESTFul API actions:"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for value in state.cities:
        cities.append(value.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities(city_id):
    """Retrieves a City object"""
    try:
        return jsonify(storage.get(City, city_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object:"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.is_json:
        data_HTTP = request.get_json()
        if 'name' in data_HTTP:
            data_HTTP['state_id'] = state_id
            new_city = City(**data_HTTP)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        abort(400, 'Missing name')
    abort(400, 'Not a JSON')    


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

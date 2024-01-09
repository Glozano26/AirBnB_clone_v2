#!/usr/bin/python3
"""Same as State, create a new view for City objects that handles
all default RESTFul API actions:"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities():
    """Retrieves the list of all City objects of a State"""
    all_cities = City.query.all()
    cities = [city.serialize() for city in all_cities]


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
    storage.delete(city_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')

        data_HTTP = request.get_json()
    if 'name' not in data_HTTP.keys():
        abort(400, 'Missing name')

    new_Cities = City(**data_HTTP)
    storage.new(new_Cities)
    storage.save()
    return jsonify(new_Cities.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Not found'}), 404
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    cities_HTTP = request.get_json()
    keys_ignored = {'id', 'state_id', 'created_at', 'updated_at'}

    for key, value in cities_HTTP.items():
        if key not in keys_ignored:
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200

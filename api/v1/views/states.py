#!/usr/bin/python3
"""Create a new view for State objects that handles all default
RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """Retrieves all State objects"""
    all_states = State.query.all()
    states = [state.serialize() for state in all_states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object by state_id"""
    try:
        state = storage.get(State, state_id)
        if state is None:
            return jsonify(state.to_dict())
    except Exception:
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    """function that removes a State object if it is not linked
    or scrambles an empty dictionary"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """transforms HTTP request body into a dictionary"""
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data.keys():
        abort(400, 'Missing name')

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def update_state_data(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    return jsonify({'error': 'Not a JSON'}), 400

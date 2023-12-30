#!/usr/bin/python3
"""Create a new view for State objects that handles all default
RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort
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
    state = State.query.filter_by(id=state_id).first()
    # state = [state for state in states if state['id'] == state_id]
    if len(state) == 0:
        abort(404)
    return jsonify(state.serialize())

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    """function that removes a State object if it is not linked
    or scrambles an empty dictionary"""
    state = storage.get(State, state_id)
    if len(state) == 0:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({}), 200



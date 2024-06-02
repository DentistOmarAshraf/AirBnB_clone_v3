#!/usr/bin/python3
"""
States API
"""
from .__init__ import app_views
from models import storage
from models.state import State
from flask import make_response, request, abort
from json import dumps


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def get_states():
    data = [state.to_dict() for state in storage.all(State).values()]
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_states():
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if 'name' not in data:
        return make_response("Missing name", 400)
    new_state = State(**data)
    new_state.save()
    res = make_response(dumps(new_state.to_dict(), indent=4), 201)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_states_id(state_id):
    data = storage.get(State, state_id)
    if data is None:
        abort(404)
    res = make_response(dumps(data.to_dict(), indent=3), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        storage.delete(city)
    storage.delete(state)
    storage.save()
    res = make_response(dumps({}), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_state_id(state_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    changed = False
    for k, v in data.items():
        x = ['id', 'created_at', 'updated_at']
        if k not in x:
            setattr(state, k, v)
            changed = True
    if changed is False:
        abort(400)
    to_ret = state.to_dict()
    storage.save()
    res = make_response(dumps(to_ret, indent=3), 200)
    res.headers['Content-type'] = 'application/json'
    return res

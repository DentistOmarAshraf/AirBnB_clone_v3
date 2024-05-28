#!/usr/bin/python3
"""
States API
"""
from .__init__ import app_views
from models import storage
from models.state import State
from flask import make_response, request, abort
import json


@app_views.route("/states", strict_slashes=False, methods=['GET', 'POST'])
@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def about_states(state_id=None):
    if state_id is None:
        if request.method == 'GET':
            data = [state.to_dict() for state in storage.all(State).values()]
            res = make_response(json.dumps(data, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'POST':
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)
            if 'name' not in data:
                return make_response("Missing name", 400)
            new_state = State(**data)
            new_state.save()
            res = make_response(json.dumps(new_state.to_dict(), indent=4), 201)
            res.headers['Content-type'] = 'application/json'
            return res

    else:
        if request.method == 'GET':
            data = []
            for state in storage.all(State).values():
                if state_id == state.id:
                    data.append(state.to_dict())
            if len(data) == 0:
                abort(404)
            res = make_response(json.dumps(data[0], indent=3), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'DELETE':
            deleted = False
            for state in storage.all(State).values():
                if state_id == state.id:
                    for city in state.cities:
                        storage.delete(city)
                    storage.delete(state)
                    storage.save()
                    deleted = True
                    break
            if deleted is False:
                abort(404)
            res = make_response(json.dumps({}), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'PUT':
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)

            changed = False
            for state in storage.all(State).values():
                if state_id == state.id:
                    for k, v in data.items():
                        x = ['id', 'created_at', 'updated_at']
                        if k not in x:
                            setattr(state, k, v)
                    changed = True
                    to_ret = state.to_dict()
                    storage.save()
            if changed is False:
                abort(404)
            res = make_response(json.dumps(to_ret, indent=3), 200)
            res.headers['Content-type'] = 'application/json'
            return res

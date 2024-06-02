#!/usr/bin/python3
"""
City API
"""

from .__init__ import app_views
from models import storage
from models.city import City
from models.state import State
from flask import make_response, abort, request
from json import dumps


@app_views.route("/cities", strict_slashes=False, methods=['GET'])
def get_cities():
    data = [city.to_dict() for city in storage.all(City).values()]
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_cities_id(city_id):
    data = storage.get(City, city_id)
    if data is None:
        abort(404)
    data = data.to_dict()
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_cities_id(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    res = make_response(dumps({}), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def put_cities_id(city_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    change = False
    for k, v in data.items():
        x = ['id', 'created_at', 'updated_at']
        if k not in x:
            setattr(city, k, v)
            change = True
    if change is False:
        abort(400)

    storage.save()
    to_ret = city.to_dict()

    res = make_response(dumps(to_ret, indent=3), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def cities_by_state(state_id=None):
    all_state = storage.get(State, state_id)
    if all_state is None:
        abort(404)
    data = [city.to_dict() for city in all_state.cities]
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def post_cities_in_state(state_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if 'name' not in data:
        return make_response("Missing name", 400)

    the_st = storage.get(State, state_id)
    if the_st is None:
        abort(404)
    new_city = City(**data)
    the_st.cities.append(new_city)
    storage.save()
    to_ret = new_city.to_dict()
    if 'state' in to_ret:
        del (to_ret['state'])
    res = make_response(dumps(to_ret, indent=4), 201)
    res.headers['Content-type'] = 'application/json'
    return res

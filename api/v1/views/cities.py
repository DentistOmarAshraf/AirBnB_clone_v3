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
@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def about_cities(city_id=None):
    if not city_id:
        if request.method == 'GET':
            data = [city.to_dict() for city in storage.all(City).values()]
            res = make_response(dumps(data, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res
    else:
        if request.method == 'GET':
            found = False
            for city in storage.all(City).values():
                if city_id == city.id:
                    data = city.to_dict()
                    found = True
            if found is False:
                abort(404)
            res = make_response(dumps(data, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'DELETE':
            deleted = False
            for city in storage.all(City).values():
                if city_id == city.id:
                    storage.delete(city)
                    storage.save()
                    deleted = True
            if deleted is False:
                abort(404)
            res = make_response(dumps({}), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'PUT':
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)

            change = False
            for city in storage.all(City).values():
                if city_id == city.id:
                    for k, v in data.items():
                        x = ['id', 'created_at', 'updated_at']
                        if k not in x:
                            setattr(city, k, v)
                    change = True
                    to_ret = city.to_dict()
                    storage.save()

            if change is False:
                abort(404)
            res = make_response(dumps(to_ret, indent=3), 200)
            res.headers['Content-type'] = 'application/json'
            return res


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(state_id=None):
    if request.method == 'GET':
        all_state = []
        for st in storage.all(State).values():
            if state_id == st.id:
                all_state.append(st)
        if len(all_state) == 0:
            abort(404)
        data = [city.to_dict() for city in all_state[0].cities]
        res = make_response(dumps(data, indent=4), 200)
        res.headers['Content-type'] = 'application/json'
        return res

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)

        if 'name' not in data:
            return make_response("Missing name", 400)

        the_st = []
        for st in storage.all(State).values():
            if st.id == state_id:
                the_st.append(st)
        if len(the_st) == 0:
            abort(404)
        new_city = City(**data)
        the_st[0].cities.append(new_city)
        storage.save()
        to_ret = new_city.to_dict()
        if 'state' in to_ret:
            del (to_ret['state'])
        res = make_response(dumps(to_ret, indent=4), 201)
        res.headers['Content-type'] = 'application/json'
        return res

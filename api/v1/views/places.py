#!/usr/bin/python3
"""
Place API
"""

from .__init__ import app_views
from flask import make_response, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from json import dumps


@app_views.route("/places", strict_slashes=False, methods=['GET'])
@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_about(place_id=None):
    if not place_id:
        if request.method == 'GET':
            data = [place.to_dict() for place in storage.all(Place).values()]
            res = make_response(dumps(data, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

    else:
        if request.method == 'GET':
            data = []
            for place in storage.all(Place).values():
                if place.id == place_id:
                    data.append(place.to_dict())
            if len(data) == 0:
                abort(404)
            res = make_response(dumps(data[0], indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'DELETE':
            dlt = False
            for place in storage.all(Place).values():
                if place_id == place.id:
                    dlt = True
                    storage.delete(place)
                    storage.save()
            if dlt is False:
                abort(404)
            res = make_response(dumps({}), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'PUT':
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)

            found = False
            for place in storage.all(Place).values():
                if place_id == place.id:
                    found = True
                    for k, v in data.items():
                        x = ['id', 'user_id', 'city_id', 'created_at',
                             'updated_at']
                        if k not in x:
                            setattr(place, k, v)
                    to_ret = place.to_dict()
                    storage.save()
            if found is False:
                abort(404)
            res = make_response(dumps(to_ret, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET', 'POST'])
def place_in_city(city_id=None):
    if request.method == 'GET':
        found = False
        for city in storage.all(City).values():
            if city_id == city.id:
                found = True
                dt = city.places
        if found is False:
            abort(404)
        dt = [x.to_dict() for x in dt]
        res = make_response(dumps(dt, indent=4), 200)
        res.headers['Content-type'] = 'application/json'
        return res

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)

        if 'user_id' not in data:
            return make_response("Missing user_id", 400)
        if 'name' not in data:
            return make_response("Missing name", 400)

        found = False
        for city in storage.all(City).values():
            if city_id == city.id:
                found = True
                the_city = city
        if found is False:
            abort(404)

        found = False
        for user in storage.all(User).values():
            if data["user_id"] == user.id:
                found = True
        if found is False:
            abort(404)

        the_place = Place(**data)
        the_city.places.append(the_place)
        the_place.save()
        to_ret = the_place.to_dict()
        if 'cities' in to_ret:
            del (to_ret['cities'])
        res = make_response(dumps(to_ret, indent=4), 201)
        res.headers['Content-type'] = 'application/json'
        return res

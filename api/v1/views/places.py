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
            data = storage.get(Place, place_id)
            if data is None:
                abort(404)
            data = data.to_dict()
            res = make_response(dumps(data, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'DELETE':
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            for review in place.reviews:
                storage.delete(review)
            storage.delete(place)
            storage.save()
            res = make_response(dumps({}), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == 'PUT':
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)

            place = storage.get(Place, place_id)
            if place is None:
                abort(404)

            found = False
            for k, v in data.items():
                x = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
                if k not in x:
                    setattr(place, k, v)
                    found = True
            if found is False:
                abort(404)

            to_ret = place.to_dict()
            storage.save()
            res = make_response(dumps(to_ret, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET', 'POST'])
def place_in_city(city_id=None):
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        dt = city.places
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

        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        user = storage.get(User, data["user_id"])
        if user is None:
            abort(404)

        the_place = Place(**data)
        city.places.append(the_place)
        user.places.append(the_place)
        the_place.save()
        to_ret = the_place.to_dict()
        print(to_ret)
        if 'cities' in to_ret:
            del (to_ret['cities'])
        if 'user' in to_ret:
            del (to_ret['user'])
        res = make_response(dumps(to_ret, indent=4), 201)
        res.headers['Content-type'] = 'application/json'
        return res

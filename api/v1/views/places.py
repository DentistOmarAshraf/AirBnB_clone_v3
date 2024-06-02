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
from models.state import State
from models.amenity import Amenity
from json import dumps


@app_views.route("/places", strict_slashes=False, methods=['GET', 'POST'])
def get_places():
    data = [place.to_dict() for place in storage.all(Place).values()]
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['GET'])
def get_places_id(place_id):
    data = storage.get(Place, place_id)
    if data is None:
        abort(404)
    data = data.to_dict()
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def del_places_id(place_id):
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


@app_views.route("places/<place_id>", strict_slashes=False, methods=['PUT'])
def put_places_id(place_id):
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
                 methods=['GET'])
def place_in_city(city_id=None):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    dt = city.places
    dt = [x.to_dict() for x in dt]
    res = make_response(dumps(dt, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_places(city_id):
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
    if 'cities' in to_ret:
        del (to_ret['cities'])
    if 'user' in to_ret:
        del (to_ret['user'])
    res = make_response(dumps(to_ret, indent=4), 201)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/places_search", strict_slashes=False, methods=['POST'])
def place_search():
    """ THIS ROUTE IS WORKING WRONG I WILL MODIFY IT LATER"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if len(data) == 0:
        return make_response(place_about(place_id=None))

    empty = True
    for k, v in data.items():
        if len(v) > 0:
            empty = False
            break
    if empty:
        return make_response(place_about(place_id=None))

    to_ret = []
    for key, val in data.items():
        if key == 'states':
            for st_id in val:
                the_state = storage.get(State, st_id)
                if the_state is None:
                    continue
                for city in the_state.cities:
                    for place in city.places:
                        if place not in to_ret:
                            to_ret.append(place)
        if key == 'cities':
            for ct_id in val:
                the_city = storage.get(City, st_id)
                if the_city is None:
                    continue
                for place in city.places:
                    if place not in to_ret:
                        to_ret.append(place)

        if key == 'amenities' and len(val) != 0:
            for amen_id in val:
                the_amen = storage.get(Amenity, amen_id)
                if the_amen is None:
                    continue
                for place in to_ret:
                    if the_amen in place.amenities:
                        continue
                    else:
                        to_ret.remove(place)

    to_ret = [x.to_dict() for x in to_ret]
    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res

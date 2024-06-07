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
    """ MAY BE SOLVED"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if len(data) == 0:
        return make_response(get_places())

    to_ret = []
    if "states" not in data.items():
        to_ret += get_places().get_json()

    for key, value in data.items():
        if key == "states":
            if len(value) == 0:
                to_ret += get_places().get_json()
            else:
                for state_id in value:
                    state = storage.get(State, state_id)
                    for city in state.cities:
                        for place in city.places:
                            if place not in to_ret:
                                to_ret.append(place.to_dict())

        if key == "cities":
            for city_id in value:
                city = storage.get(City, city_id)
                for place in city.places:
                    if place.to_dict() not in to_ret:
                        to_ret.append(place.to_dict())

        if key == "amenities":
            to_rem = []
            for amen_id in value:
                amen = storage.get(Amenity, amen_id)
                for place_dic in to_ret:
                    place = storage.get(Place, place_dic["id"])
                    if amen not in place.amenities:
                        to_rem.append(place_dic)

            for x in to_rem:
                if x in to_ret:
                    to_ret.remove(x)

    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res

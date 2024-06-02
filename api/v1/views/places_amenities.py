#!/usr/bin/python3
"""
Place Amenity API
"""

from .__init__ import app_views
from flask import Flask, abort, make_response
from flask import request
from models import storage
from models.place import Place
from models.amenity import Amenity
from json import dumps


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def get_amenities_in_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    to_ret = []
    for amenity in place.amenities:
        to_ret.append(amenity.to_dict())
    res = make_response(dumps(to_ret, indent=3), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['GET'])
def get_amenities_id(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    res = make_response(dumps(amenity.to_dict(), indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def del_amenities_from_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    res = make_response(dumps({}), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def add_amenities_to_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        res = make_response(dumps(amenity.to_dict(), indent=4), 200)

    else:
        place.amenities.append(amenity)
        storage.save()
        res = make_response(dumps(amenity.to_dict(), indent=4), 201)

    res.headers['Content-type'] = 'application/json'
    return res

#!/usr/bin/python3
"""
Review API
"""

from .__init__ import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from json import dumps
from flask import abort, make_response, request


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_places_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = []
    for rev in place.reviews:
        data.append(rev.to_dict())
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_places_reviews(place_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if 'user_id' not in data:
        return make_response("Missing user_id", 400)
    if 'text' not in data:
        return make_response("Missing text", 400)

    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)

    the_user = storage.get(User, data['user_id'])
    if the_user is None:
        abort(404)

    the_rev = Review(**data)
    the_place.reviews.append(the_rev)
    the_user.reviews.append(the_rev)
    the_rev.save()
    to_ret = the_rev.to_dict()
    if 'place' in to_ret:
        del (to_ret['place'])
    if 'user' in to_ret:
        del (to_ret['user'])
    res = make_response(dumps(to_ret, indent=4), 201)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    data = storage.get(Review, review_id)
    if data is None:
        abort(404)
    data = data.to_dict()
    res = make_response(dumps(data, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_review_id(review_id):
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    storage.delete(rev)
    storage.save()
    res = make_response(dumps({}), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review_id(review_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if 'text' not in data:
        return make_response("Missing text", 400)

    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    change = False
    for k, v in data.items():
        x = ['id', 'user_id', 'created_at', 'updated_at']
        if k not in x:
            setattr(rev, k, v)
            change = True
    if change is False:
        abort(404)

    rev.save()
    to_ret = rev.to_dict()
    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res

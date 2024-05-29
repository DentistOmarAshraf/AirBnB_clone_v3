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


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET', 'POST'])
def place_rev(place_id=None):
    if request.method == "GET":
        data = []
        found = False
        for place in storage.all(Place).values():
            if place_id == place.id:
                for rev in place.reviews:
                    data.append(rev.to_dict())
                found = True
        if found is False:
            abort(404)
        res = make_response(dumps(data, indent=4), 200)
        res.headers['Content-type'] = 'application/json'
        return res

    if request.method == "POST":
        try:
            data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)

        if 'user_id' not in data:
            return make_response("Missing user_id", 400)
        if 'text' not in data:
            return make_response("Missing text", 400)

        found = False
        for place in storage.all(Place).values():
            if place_id == place.id:
                found = True
                the_place = place
        if found is False:
            abort(404)

        found = False
        for user in storage.all(User).values():
            if data['user_id'] == user.id:
                found = True
                the_user = user
        if found is False:
            abort(404)

        the_rev = Review(**data)
        the_place.reviews.append(the_rev)
        the_user.reviews.append(the_rev)
        the_rev.save()
        to_ret = the_rev.to_dict()
        print(to_ret)
        if 'place' in to_ret:
            del (to_ret['place'])
        if 'user' in to_ret:
            del (to_ret['user'])
        res = make_response(dumps(to_ret, indent=4), 201)
        res.headers['Content-type'] = 'application/json'
        return res


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_about(review_id=None):
    if review_id:
        if request.method == "GET":
            data = []
            for rev in storage.all(Review).values():
                if rev.id == review_id:
                    data.append(rev.to_dict())

            if len(data) == 0:
                abort(404)

            res = make_response(dumps(data[0], indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == "DELETE":
            dlt = False
            for rev in storage.all(Review).values():
                if rev.id == review_id:
                    storage.delete(rev)
                    storage.save()
                    dlt = True
            if dlt is False:
                abort(404)
            res = make_response(dumps({}), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == "PUT":
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)

            if 'text' not in data:
                return make_response("Missing text", 400)
            if 'user_id' not in data:
                return make_response("Missing user_id", 400)

            change = False
            for rev in storage.all(Review).values():
                if rev.id == review_id:
                    for k, v in data.items():
                        x = ['id', 'user_id', 'created_at', 'updated_at']
                        if k not in x:
                            setattr(rev, k, v)
                    change = True
                    rev.save()
                    to_ret = rev.to_dict()

                if change is False:
                    abort(404)

                res = make_response(dumps(to_ret, indent=4), 200)
                res.headers['Content-type'] = 'application/json'
                return res

#!/usr/bin/python3
"""
Amenity API
"""

from .__init__ import app_views
from models import storage
from models.amenity import Amenity
from flask import make_response, abort, request
from json import dumps


@app_views.route("/amenities", strict_slashes=False, methods=['GET', 'POST'])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_about(amenity_id=None):
    if not amenity_id:
        if request.method == "GET":
            data = [amen.to_dict() for amen in storage.all(Amenity).values()]
            res = make_response(dumps(data, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == "POST":
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)
            if 'name' not in data:
                return make_response("Missing name", 400)

            new_amen = Amenity(**data)
            new_amen.save()
            res = make_response(dumps(new_amen.to_dict(), indent=4), 201)
            res.headers['Content-type'] = 'application/json'
            return res

    else:
        if request.method == "GET":
            data = storage.get(Amenity, amenity_id)
            if data is None:
                abort(404)
            data = data.to_dict()
            res = make_response(dumps(data, indent=3), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == "DELETE":
            amen = storage.get(Amenity, amenity_id)
            if amen is None:
                abort(404)
            storage.delete(amen)
            storage.save()

            res = make_response(dumps({}), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == "PUT":
            try:
                data = request.get_json()
            except Exception:
                return make_response("Not a JSON", 400)

            amen = storage.get(Amenity, amenity_id)
            if amen is None:
                abort(404)

            for k, v in data.items():
                x = ['id', 'created_at', 'updated_at']
                if k not in x:
                    setattr(amen, k, v)
            storage.save()
            to_ret = amen.to_dict()

            res = make_response(dumps(to_ret, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

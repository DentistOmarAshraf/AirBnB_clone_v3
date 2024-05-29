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
            data = []
            for amen in storage.all(Amenity).values():
                if amen.id == amenity_id:
                    data.append(amen.to_dict())
            if len(data) == 0:
                abort(404)

            res = make_response(dumps(data[0], indent=3), 200)
            res.headers['Content-type'] = 'application/json'
            return res

        if request.method == "DELETE":
            dlt = False
            for amen in storage.all(Amenity).values():
                if amen.id == amenity_id:
                    storage.delete(amen)
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

            change = False
            for amen in storage.all(Amenity).values():
                if amen.id == amenity_id:
                    for k, v in data.items():
                        x = ['id', 'created_at', 'updated_at']
                        if k not in x:
                            setattr(amen, k, v)
                    storage.save()
                    to_ret = amen.to_dict()
                    change = True

            if change is False:
                abort(404)
            res = make_response(dumps(to_ret, indent=4), 200)
            res.headers['Content-type'] = 'application/json'
            return res

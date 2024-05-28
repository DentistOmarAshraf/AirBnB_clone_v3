#!/usr/bin/python3
"""
blueprint Routes
"""

from .__init__ import app_views
from flask import make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status_app():
    """return Status of server"""
    data = {"status": "OK"}
    res = make_response(json.dumps(data, indent=2), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def count_inDB():
    """return Number of instance in each table"""
    data = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    res = make_response(json.dumps(data, indent=2), 200)
    res.headers['Content-type'] = 'application/json'
    return res

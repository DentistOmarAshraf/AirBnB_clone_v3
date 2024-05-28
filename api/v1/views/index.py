#!/usr/bin/python3
"""
blueprint Routes
"""

from .__init__ import app_views
from flask import make_response
import json


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status_app():
    """return Status of server"""
    data = {"status": "OK"}
    res = make_response(json.dumps(data, indent=2), 200)
    res.headers['Content-type'] = 'application/json'
    return res

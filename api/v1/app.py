#!/usr/bin/python3
"""
Rest API Master
"""

from flask import Flask, make_response
from flask_cors import CORS
from .views import app_views
from os import getenv
from models import storage
import json


app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, origins=["0.0.0.0"])


@app.teardown_appcontext
def close_db(exceptions):
    """remove DB session"""
    storage.close()


@app.errorhandler(404)
def handle(error):
    data = {
            "error": "Not found"
            }
    res = make_response(json.dumps(data, indent=4), 404)
    res.headers['Content-type'] = 'application/json'
    return res


if __name__ == "__main__":
    """
    Start API
    """
    Host = getenv("HBNB_API_HOST")
    Port = getenv("HBNB_API_PORT")

    if Host and Port:
        app.run(host=Host, port=Port, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)

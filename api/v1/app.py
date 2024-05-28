#!/usr/bin/python3
"""
Rest API Master
"""

from flask import Flask
from .views import app_views
from os import getenv
from models import storage


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exceptions):
    """remove DB session"""
    storage.close()


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

#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('blueprint', __name__, url_prefix='/api/v1')

from .index import *

#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('blueprint', __name__, url_prefix='/api/v1')

from .index import *
from .states import *
from .cities import *
from .amenities import *
from .users import *
from .places import *
from .places_reviews import *

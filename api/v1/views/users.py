#!/usr/bin/python3
"""
User API
"""
from .__init__ import app_views
from models import storage
from models.user import User
from flask import make_response, request, abort
from json import dumps


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def get_users():
    data = [usr.to_dict() for usr in storage.all(User).values()]
    res = make_response(dumps(data, indent=3), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_users():
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if 'email' not in data:
        return make_response("Missing email", 400)
    if 'password' not in data:
        return make_response("Missing password", 400)

    new_usr = User(**data)
    new_usr.save()
    res = make_response(dumps(new_usr.to_dict(), indent=3), 201)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
def get_users_id(user_id):
    data = storage.get(User, user_id)
    if data is None:
        abort(404)
    data = data.to_dict()

    res = make_response(dumps(data, indent=3), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def put_users_id(user_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    usr = storage.get(User, user_id)
    if usr is None:
        abort(404)
    change = False
    for k, v in data.items():
        x = ['id', 'email', 'created_at', 'updated_at']
        if k not in x:
            setattr(usr, k, v)
            change = True
    if change is False:
        abort(400)
    storage.save()
    to_ret = usr.to_dict()
    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers['Content-type'] = 'application/json'
    return res


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['DELETE'])
def del_users_id(user_id):
    usr = storage.get(User, user_id)
    if usr is None:
        abort(404)
    storage.delete(usr)
    storage.save()

    res = make_response(dumps({}), 200)
    res.headers['Content-type'] = 'application/json'
    return res

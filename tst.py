#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/users/
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/users/", data={ 'email': "f@f.com", 'password': "pwdf", 'first_name': "fnf", 'last_name': "lnf" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)

#!/usr/bin/python3
"""handle all the status and stats request"""
from api.v1.views import app_views
from flask import jsonify
from models import storage as s


@app_views.route('/status', strict_slashes=False)
def status():
    """return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns the stats of the storage"""
    count = {
            "amenities": s.count('Amenity'),
            "cities": s.count('City'),
            "places": s.count('Place'),
            "reviews": s.count('Review'),
            "states": s.count('State'),
            "users": s.count('User')
            }
    return jsonify(count)

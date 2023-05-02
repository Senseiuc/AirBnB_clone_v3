#!/usr/bin/python3
"""
handles the places requests
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage as s
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """gets places of a city"""
    city = s.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    """gets a place"""
    place = s.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place"""
    place = s.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    s.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a new place"""
    city = s.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dict = request.get_json()
    if 'user_id' not in dict:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = s.get("User", dict['user_id'])
    if user is None:
        abort(404)
    if 'name' not in dict:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    dict['city_id'] = city_id
    place = Place(**dict)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates a place"""
    place = s.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches place"""
    if request.get_json() is not None:
        vals = request.get_json()
        states = vals.get('states', [])
        cities = vals.get('cities', [])
        amenities = vals.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = s.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = s.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = s.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = s.get('City', city_id)
                for place in city.places:
                    places.append(place)
        conf_places = []
        for place in places:
            place_amenities = place.amenities
            conf_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    conf_places.pop()
                    break
        return jsonify(conf_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

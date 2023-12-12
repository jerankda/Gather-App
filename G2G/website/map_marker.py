from flask import Blueprint, request, jsonify, render_template
from .models import Marker
from . import db

map_marker = Blueprint('map_marker', __name__)

# Adding pins on the map
@map_marker.route('/add_marker', methods=['POST'])
def add_marker():
    if request.method == 'POST':
        data = request.json
        lat = data['lat']
        lng = data['lng']
        name = data['name']

        new_marker = Marker(lat=lat, lng=lng, name = name)
        db.session.add(new_marker)
        db.session.commit()

        return jsonify({'message': 'Marker added successfully'})

# Giving the map the location and name of all already set pins
@map_marker.route('/get_markers')
def get_markers():
    markers = Marker.query.all()
    markers_data = [{'lat': marker.lat, 'lng': marker.lng, 'name': marker.name} for marker in markers]
    return jsonify(markers_data)


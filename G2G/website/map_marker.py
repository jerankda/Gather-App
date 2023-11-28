from flask import Blueprint, request, jsonify
from .models import Marker
from . import db
 
map_marker = Blueprint('map_marker', __name__)
 
#adding pins on the map
@map_marker.route('/add_marker', methods=['POST'])
def add_marker():
    if request.method == 'POST':
        data = request.json
        name = data['name']
        lat = data['lat']
        lng = data['lng']
 
        new_marker = Marker(name=name, lat=lat, lng=lng)
        db.session.add(new_marker)
        db.session.commit()
 
 
        return jsonify({'message': 'Marker added successfully'})
   
#giving the map the location and name of all already set pins
@map_marker.route('/get_markers')
def get_markers():
 
    markers = Marker.query.all()
    markers_data = [{'name': marker.name, 'lat': marker.lat, 'lng': marker.lng} for marker in markers]
    return jsonify(markers_data)
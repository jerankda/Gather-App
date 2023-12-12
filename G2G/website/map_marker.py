from flask import Blueprint, request, jsonify, render_template
from .models import Marker, Gather
from . import db

map_marker = Blueprint('map_marker', __name__)


# Giving the map the location and name of all already set pins
@map_marker.route('/get_markers')
def get_markers():
    markers = Marker.query.all()
    markers_data = [{'lat': marker.lat, 'lng': marker.lng, 'name': marker.gather.name} for marker in markers]
    return jsonify(markers_data)


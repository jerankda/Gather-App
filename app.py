from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///markers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('gather_maps.html')

@app.route('/get_markers')
def get_markers():
    markers = Marker.query.all()
    markers_data = [{'name': marker.name, 'lat': marker.lat, 'lng': marker.lng} for marker in markers]
    return jsonify(markers_data)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    data = request.json
    name = data['name']
    lat = data['lat']
    lng = data['lng']

    new_marker = Marker(name=name, lat=lat, lng=lng)
    db.session.add(new_marker)
    db.session.commit()

    return jsonify({'message': 'Marker added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
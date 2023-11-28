from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#creating Database for login details
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Gather(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    location = db.Column(db.String(1000))

    #creating a Database for the map pins
class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
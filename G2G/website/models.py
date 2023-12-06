from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#creating a association between gathers and users
user_gather_association = db.Table(
    'user_gather_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('gather_id', db.Integer, db.ForeignKey('gather.id'))
)

#creating Database for login details
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    Gathers = db.relationship('Gather', secondary=user_gather_association, back_populates='users')
   
#creating a Database for the Gathers
class Gather(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Host = db.Column(db.String(20))
    users = db.relationship('User', secondary=user_gather_association, back_populates='Gathers')

#creating a Database for the map pins
class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)


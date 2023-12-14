from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

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
    Date = db.Column(db.Date)
    Time = db.Column(db.Time)
    createdAt = db.Column(db.DateTime(),default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Host = db.Column(db.String(20))
    users = db.relationship('User', secondary=user_gather_association, back_populates='Gathers')
    markers = db.relationship('Marker', back_populates='gather')
    

#creating a Database for the map pins
class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float) 
    lng = db.Column(db.Float)
    gather_id = db.Column(db.Integer, db.ForeignKey('gather.id'))
    gather = db.relationship('Gather', back_populates='markers')

#creating a Database for the messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    

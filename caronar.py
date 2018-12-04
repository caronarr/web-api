from os import environ, path, pardir

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

basedir = path.abspath(path.join(__file__, pardir))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or \
        'sqlite:///' + path.join(basedir, 'caronar.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    photo = db.Column(db.String(256))


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'phone', 'photo')


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)


class LocationSchema(ma.Schema):
    class Meta:
        fields = ('name', 'latitude', 'longitude')


class DriverOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    driver = db.relationship("User")
    scheduled_time = db.Column(db.DateTime)
    origin_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    origin = db.relationship("Location", foreign_keys=[origin_id])
    destination_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    destination = db.relationship("Location", foreign_keys=[destination_id])
    requested_tip = db.Column(db.Float)


class DriverOfferSchema(ma.Schema):
    class Meta:
        fields = ('id', 'driver', 'scheduled_time', 'origin', 'destination', 'requested_tip')


class RiderOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rider = db.relationship("User")
    scheduled_time = db.Column(db.DateTime)
    origin_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    origin = db.relationship("Location", foreign_keys=[origin_id])
    destination_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    destination = db.relationship("Location", foreign_keys=[destination_id])
    offered_tip = db.Column(db.Float)


class RiderOfferSchema(ma.Schema):
    class Meta:
        fields = ('id', 'rider', 'scheduled_time', 'origin', 'destination', 'offered_tip')


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_offer_id = db.Column(db.Integer, db.ForeignKey('driver_offer.id'), index=True)
    driver_offer = db.relationship("DriverOffer")
    rider_offer_id = db.Column(db.Integer, db.ForeignKey('rider_offer.id'), index=True)
    rider_offer = db.relationship("RiderOffer")
    agreed_tip = db.Column(db.Float)


class DealSchema(ma.Schema):
    class Meta:
        fields = ('id', 'driver_offer', 'rider_offer', 'agreed_tip')


# Parsers
user_schema = UserSchema()
users_schema = UserSchema(many=True)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
driver_offer_schema = DriverOfferSchema()
driver_offers_schema = DriverOfferSchema(many=True)
rider_offer_schema = RiderOfferSchema()
rider_offers_schema = RiderOfferSchema(many=True)

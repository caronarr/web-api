from os import environ, path, pardir

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, fields, reqparse
from datetime import timezone, datetime

from rest_crud import add_collection

basedir = path.abspath(path.join(__file__, pardir))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or \
        'sqlite:///' + path.join(basedir, 'caronar.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    photo = db.Column(db.String(256))

    @staticmethod
    def json():
        return {
            'id': fields.Integer,
            'name': fields.String,
            'phone': fields.String,
            'photo': fields.String
        }

    @staticmethod
    def req_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('photo')
        parser.add_argument('phone')
        return parser


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)

    @staticmethod
    def json():
        return {
            'id': fields.Integer,
            'name': fields.String,
            'latitude': fields.Float,
            'longitude': fields.Float
        }

    @staticmethod
    def req_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('latitude')
        parser.add_argument('longitude')
        return parser


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

    @staticmethod
    def json():
        return {
            'id': fields.Integer,
            'driver': fields.Nested(User.json()),
            'origin': fields.Nested(Location.json()),
            'destination': fields.Nested(Location.json()),
            'scheduled_time': fields.DateTime,
            'requested_tip': fields.Float
        }

    @staticmethod
    def req_parser():

        parser = reqparse.RequestParser()
        parser.add_argument('driver', type=model_parser(User, require_created=True), required=True)
        parser.add_argument('origin', type=model_parser(Location), required=True)
        parser.add_argument('destination', type=model_parser(Location), required=True)
        parser.add_argument('scheduled_time', type=datetime, required=True)
        parser.add_argument('requested_tip')
        return parser


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

    @staticmethod
    def json():
        return {
            'id': fields.Integer,
            'rider': fields.Nested(User.json()),
            'origin': fields.Nested(Location.json()),
            'destination': fields.Nested(Location.json()),
            'scheduled_time': fields.DateTime,
            'offered_tip': fields.Float
        }

    @staticmethod
    def req_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('rider', type=model_parser(User, require_created=True), required=True)
        parser.add_argument('origin', type=model_parser(Location), required=True)
        parser.add_argument('destination', type=model_parser(Location), required=True)
        parser.add_argument('scheduled_time', type=datetime, required=True)
        parser.add_argument('offered_tip')
        return parser


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_offer_id = db.Column(db.Integer, db.ForeignKey('driver_offer.id'), index=True)
    driver_offer = db.relationship("DriverOffer")
    rider_offer_id = db.Column(db.Integer, db.ForeignKey('rider_offer.id'), index=True)
    rider_offer = db.relationship("RiderOffer")
    agreed_tip = db.Column(db.Float)

    @staticmethod
    def json():
        return {
            'id': fields.Integer,
            'driver_offer': fields.Nested(DriverOffer.json()),
            'rider_offer': fields.Nested(RiderOffer.json()),
            'agreed_tip': fields.Float
        }

    @staticmethod
    def req_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('driver_offer', type=model_parser(DriverOffer, require_created=True))
        parser.add_argument('rider_offer', type=model_parser(RiderOffer, require_created=True))
        parser.add_argument('agreed_tip', type=float)
        return parser


# parsers
def model_parser(model, require_created=False):
    def p(value, name):
        if require_created and 'id' not in value:
            raise ValueError('{} value requires a valid id'.format(name))
        try:
            x = model.query.get(value['id']) if 'id' in value else model(**value)
        except TypeError:
            # Raise a ValueError, and maybe give it a good error string
            raise ValueError("{}: Invalid {}".format(name, model.__name__))

        return x

    return p


# Routes
add_collection(api, db, User)
add_collection(api, db, Location)
add_collection(api, db, DriverOffer)
add_collection(api, db, RiderOffer)
add_collection(api, db, Deal)

if __name__ == '__main__':
    app.run(debug=True)

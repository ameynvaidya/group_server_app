from enum import unique
from flask_login import UserMixin
from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    secret_salt = db.Column(db.String(1000))

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    client_secret = db.Column(db.String(1000))

class UserAuthCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_code = db.Column(db.String(100), unique=True)

class UserAccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(100))
    access_token_creation_time = db.Column(db.Integer)
    access_token_expires_in = db.Column(db.Integer)
    refresh_token = db.Column(db.String(100))
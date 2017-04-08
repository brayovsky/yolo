from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context
from application.main.app import app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=True)
    bucketlists = db.relationship("Bucketlists", backref="owner",
                                  lazy="dynamic")

    def hash_password(self, password):
        return custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, return_header=True)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data[0]['id'])
        return user

    def __init__(self, username, email, password):
        # assert correct number of characters
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.username


class Bucketlists(db.Model):
    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime)
    items = db.relationship("Items", backref="bucket",
                            lazy="dynamic")

    def __init__(self, name, created_by):
        # assert correct number of characters
        self.name = name
        self.created_by = created_by
        self.date_created = datetime.now()

    def __repr__(self):
        return "<Bucketlist %r>" % self.name


class Items(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    bucketlist = db.Column(db.Integer, db.ForeignKey("bucketlists.id"),
                           nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime)

    def __init__(self, name, bucketlist):
        # assert correct number of characters
        self.name = name
        self.bucketlist = bucketlist
        self.date_created = datetime.now()

    def __repr__(self):
        return "<Item %r>" % self.name

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from passlib.apps import custom_app_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import SearchQueryMixin

from application.main.app import app

db = SQLAlchemy(app)
make_searchable()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=True)
    date_created = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.now())
    last_login = db.Column(db.DateTime)
    bucketlists = db.relationship("Bucketlists", backref="owner",
                                  lazy="dynamic")

    def hash_password(self, password):
        return custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=18000):
        serializer = Serializer(app.config['SECRET_KEY'],
                                expires_in=expiration)
        token = serializer.dumps({'id': self.id})
        return token.decode()

    # TODO: Invalid token is raising an unhandled type error
    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token, return_header=True)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data[0]['id'])
        return user

    def __init__(self, username, email, password):
        # assert correct number of characters
        self.username = username.lower()
        self.email = email
        self.password = self.hash_password(password)
        self.date_created = datetime.now()

    def __repr__(self):
        return '<User %r>' % self.username


class BucketlistsQuery(BaseQuery, SearchQueryMixin):
    pass


class Bucketlists(db.Model):
    query_class = BucketlistsQuery
    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=False)
    date_created = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.now())
    date_modified = db.Column(db.DateTime)
    items = db.relationship("Items", backref="bucket",
                            lazy="dynamic")
    search_vector = db.Column(TSVectorType('name'))

    def update_date_modified(self):
        self.date_modified = datetime.now()

    def __init__(self, name, created_by):
        # assert correct number of characters
        self.name = name.lower()
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
    date_created = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.now())
    date_modified = db.Column(db.DateTime)

    def __init__(self, name, bucketlist):
        self.name = name.lower()
        self.bucketlist = bucketlist
        self.date_created = datetime.now()

    def update_date_modified(self):
        self.date_modified = datetime.now()

    def __repr__(self):
        return "<Item %r>" % self.name

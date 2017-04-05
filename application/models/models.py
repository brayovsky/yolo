from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from passlib.apps import custom_app_context

from application.main.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))

    def hash_password(self, password):
        return custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.username

from flask import g
from flask_httpauth import HTTPBasicAuth
from marshmallow import Schema, fields

from application.models.models import User, Bucketlists, Items

auth = HTTPBasicAuth()


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    date_created = fields.DateTime()
    last_login = fields.DateTime()

user_schema = UserSchema()


class Verify:
    """Holds methods for verifying input data from the user"""
    @staticmethod
    def verify_id_is_int(val, abort=False):
        pass

    @staticmethod
    def verify_bucketlist_exists(bucketlist_id=None, bucketlist_name=None,
                                 abort=False):
        """Verify bucketlist id or name exists in db"""
        pass

    @staticmethod
    def verify_item_exists(item_id=None, item_name=None,
                           abort=False):
        """Verify item_id exists in db"""
        pass

    @staticmethod
    @auth.verify_password
    def verify_user(username_or_token, password):
        """Verifies a valid user by a token
         or username and password
         """
        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate by username and password
            user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        return user

    @staticmethod
    def verify_valid_username(username, abort=False):
        """Verify username is a valid username"""
        pass

    @staticmethod
    def verify_user_exists(username=None, email=None,
                           abort=False):
        """Verify username exists in db"""
        pass

    @staticmethod
    def verify_valid_email(email, abort=False):
        """Verify email is a valid email"""
        pass

    @staticmethod
    def verify_user_details(user_data):
        """Verify user information using UserSchema"""
        data, errors = user_schema.load(user_data)
        if errors:
            return {"success": False,
                    "errors": errors}
        return {"success": True}

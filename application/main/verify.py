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


class BucketListSchema(Schema):
    name = fields.Str()
    created_by = fields.Int()
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    items = fields.Int()


user_schema = UserSchema()
bucketlist_schema = BucketListSchema()


class Verify:
    """Holds methods for verifying input data from the user"""
    @staticmethod
    def verify_bucketlist_exists(bucketlist_id=None, bucketlist_name=None,
                                 abort=False):
        """Verify bucketlist id or name exists in db"""
        if bucketlist_id:
            bucketlist = Bucketlists.query.get(bucketlist_id)
        elif bucketlist_name:
            bucketlist = Bucketlists.query.filter_by(name=bucketlist_name).first()
        else:
            raise TypeError("bucketlist_id or bucketlist_name arguments missing")

        if not bucketlist:
            return False
        return bucketlist

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
        g.user = user
        return True

    @staticmethod
    def verify_login(username, password):
        """Verify login details are correct"""
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return False
        user.token = user.generate_auth_token()
        return user

    @staticmethod
    def verify_user_details(user_data):
        """Verify user information using UserSchema"""
        data, errors = user_schema.load(user_data)
        if errors:
            return {"success": False,
                    "errors": errors}
        return {"success": True}

    @staticmethod
    def verify_bucketlist_details(bucketlist_data):
        data, errors = bucketlist_schema.load(bucketlist_data)
        if errors:
            return {"success": False,
                    "errors": errors}
        return {"success": True}

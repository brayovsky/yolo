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


class ItemsSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    bucketlist = fields.Int()
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Boolean()


class BucketListSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    created_by = fields.Int()
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    items = fields.Nested(ItemsSchema, many=True, exclude=('bucketlist', ))

user_schema = UserSchema()
bucketlist_schema = BucketListSchema()
items_schema = ItemsSchema()


class Verify:
    """Holds methods for verifying input data from the user"""
    @staticmethod
    def verify_bucketlist_exists(bucketlist_id=None, bucketlist_name=None):
        """Verify bucketlist id or name exists in db"""
        if bucketlist_id:
            bucketlist = Bucketlists.query.filter_by(
                id=bucketlist_id,
                created_by=g.user.id).first()
        elif bucketlist_name:
            bucketlist = Bucketlists.query.filter_by(
                name=bucketlist_name,
                created_by=g.user.id).first()
        else:
            raise TypeError(
                "bucketlist_id or bucketlist_name arguments missing")

        if not bucketlist:
            return False
        return bucketlist

    @staticmethod
    def verify_item_exists(bucketlist_id, item_id=None, item_name=None):
        """Verify item_id exists in db"""
        if item_id:
            item = Items.query.filter_by(id=item_id,
                                         bucketlist=bucketlist_id).first()
        elif item_name:
            item = Items.query.filter_by(name=item_name,
                                         bucketlist=bucketlist_id).first()
        else:
            raise TypeError(
                "bucketlist_id or bucketlist_name arguments missing")

        if not item:
            return False
        return item

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
    def check_username_exists(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return True
        return False

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
        # TODO: Check for empty strings
        data, errors = user_schema.load(user_data)
        if errors:
            return {"success": False,
                    "errors": errors}
        return {"success": True}

    @staticmethod
    def verify_bucketlist_details(bucketlist_data):
        # TODO: Check for empty strings
        data, errors = bucketlist_schema.load(bucketlist_data)
        if errors:
            return {"success": False,
                    "errors": errors}
        return {"success": True}

    @staticmethod
    def verify_item_details(item_data):
        # TODO: Check for empty strings
        data, errors = items_schema.load(item_data)
        if errors:
            return {"success": False,
                    "errors": errors}
        return {"success": True}

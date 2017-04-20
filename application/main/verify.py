from flask import g
from flask_httpauth import HTTPBasicAuth

from application.models.models import User, Bucketlists, Items

auth = HTTPBasicAuth()


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
        # if token fails, try username and password
        pass

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

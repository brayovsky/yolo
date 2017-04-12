from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api


app = Flask(__name__)
# Load configurations
app.config.from_object("application.default_settings.DevelopmentConfig")
app.config.from_envvar("YOLO_SETTINGS")

# Ignore pep8 to enable cyclic import
from application.models.models import User, Bucketlists, Items, db
from application.main.verify import Verify, auth

api = Api(app)


class Common:
    """Contains common methods for CRUD operations"""
    @staticmethod
    def add_to_db(model_obj):
        """Commits added items to the database"""
        pass

    @staticmethod
    def update_db():
        """Commits updated items to the database"""
        pass


class Login(Resource):
    """Bundles all processes from the request
       /auth/login
    """
    def post(self):
        """Logs in an existing user"""
        pass


class Register(Resource, Common):
    """Bundles all processes from the request
       /auth/register
    """
    def post(self):
        """Registers a new user"""
        # If user logged in do not register
        pass


class UserBucketlists(Resource, Common):
    """Bundles all processes from the request
       /bucketlists
    """
    @auth.login_required
    def post(self):
        """Creates a new bucketlist"""
        pass

    @auth.login_required
    def get(self):
        """Retreives all bucketlists"""
        pass


class SingleBucketlist(Resource, Common):
    """Bundles all processes from the request
       /bucketlists/<id>
    """
    @auth.login_required
    def get(self, id):
        """Retreives a single bucketlist and items"""
        pass

    @auth.login_required
    def put(self, id):
        """Updates a single bucketlist"""
        pass

    @auth.login_required
    def delete(self, id):
        """Deletes a bucketlist"""
        pass


class NewBucketListItems(Resource, Common):
    """Bundles all processes from the request
       /bucketlists/<id>/items
        """
    @auth.login_required
    def post(self, id):
        """Creates new bucketlist items for a bucketlist"""
        pass


class BucketListItems(Resource, Common):
    """Bundles all processes from the request
       /bucketlists/<id>/items/<item_id>
    """
    @auth.login_required
    def put(self, id):
        """Updates an item in a bucketlist"""
        pass

    @auth.login_required
    def delete(self, id):
        """Deletes an item in a bucketlist"""
        pass


api.add_resource(Login, "/v1/auth/login")
api.add_resource(Register, "/v1/auth/register")
api.add_resource(UserBucketlists, "/v1/bucketlists")
api.add_resource(SingleBucketlist, "/v1/bucketlists/<id>")
api.add_resource(NewBucketListItems, "/v1/bucketlists/<id>/items")
api.add_resource(BucketListItems, "/v1/bucketlists/<id>/items/<item_id>")


if __name__ == "__main__":
    app.run()

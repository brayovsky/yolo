from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Load configurations
app.config.from_object("application.default_settings.DevelopmentConfig")
app.config.from_envvar("YOLO_SETTINGS")

# Ignore pep8 to enable cyclic import
from application.models.models import User, db


class Login(Resource):
    """Bundles all processes from the request
       /auth/login
    """
    def post(self):
        """Logs in an existing user"""
        return "login"


class Register(Resource):
    """Bundles all processes from the request
       /auth/register
    """
    def post(self):
        """Registers a new user"""
        return "register"


class Bucketlists(Resource):
    """Bundles all processes from the request
       /bucketlists
    """
    def post(self):
        """Creates a new bucketlist"""
        return "new bucketlist"

    def get(self):
        """Retreives all bucketlists"""
        return "all bucketlists"


class SingleBucketlist(Resource):
    """Bundles all processes from the request
       /bucketlists/<id>
    """
    def get(self, id):
        """Retreives a single bucketlist and items"""
        return "get single bucketlist"

    def put(self, id):
        """Updates a single bucketlist"""
        return "update bucketlist"

    def delete(self, id):
        """Deletes a bucketlist"""
        return "delete bucketlist"


class NewBucketListItems(Resource):
    """Bundles all processes from the request
       /bucketlists/<id>/items
        """
    def post(self, id):
        """Creates new bucketlist items for a bucketlist"""
        return "new bucketlist items"


class BucketListItems(Resource):
    """Bundles all processes from the request
       /bucketlists/<id>/items/<item_id>
    """
    def post(self, id):
        """Creates a new item in a bucketlist"""
        return "new item in bucketlist"

    def put(self, id, item_id):
        """Updates an item in a bucketlist"""
        return "update an item in bucketlist"

    def delete(self, id, item_id):
        """Deletes an item in a bucketlist"""
        return "delete a bucketlist item"


api.add_resource(Login, "/auth/login")
api.add_resource(Register, "/auth/register")
api.add_resource(Bucketlists, "/bucketlists")
api.add_resource(SingleBucketlist, "/bucketlists/<id>")
api.add_resource(NewBucketListItems, "/bucketlists/<id>/items")
api.add_resource(BucketListItems, "/bucketlists/<id>/items/<item_id>")


if __name__ == "__main__":
    app.run()

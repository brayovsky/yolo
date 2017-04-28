from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api


app = Flask(__name__)
# Load configurations
app.config.from_object("application.default_settings.DevelopmentConfig")
app.config.from_envvar("YOLO_SETTINGS")

# Ignore pep8 to enable cyclic import
from application.models.models import User, Bucketlists, Items, db
from application.main.verify import Verify, BucketListSchema, auth

api = Api(app)
bucketlist_schema = BucketListSchema()


class Common:
    """Contains common methods for CRUD operations"""
    @staticmethod
    def add_to_db(model_obj):
        """Commits added items to the database"""
        db.session.add(model_obj)
        db.session.commit()

    @staticmethod
    def delete_db_record(model_obj):
        """Deletes a record in the database"""
        db.session.delete(model_obj)
        db.session.commit()

    @staticmethod
    def update_db():
        """Commits updated items to the database"""
        db.session.commit()


class Login(Resource):
    """Bundles all processes from the request
       /auth/login
    """
    def post(self):
        """Logs in an existing user"""
        # Send username and password
        user_data = {"username": request.form.get('username'),
                     "password": request.form.get('password')}

        # Verify correct format
        verify_data = Verify.verify_user_details(user_data)
        if not verify_data["success"]:
            return verify_data["errors"], 400

        # Log in
        user = Verify.verify_login(user_data["username"],
                                   user_data["password"])

        if not user:
            return {"message": "Invalid credentials"}, 401

        return {"user": user.username,
                "token": user.token}, 200


class Register(Resource, Common):
    """Bundles all processes from the request
       /auth/register
    """
    def post(self):
        """Registers a new user"""
        user_data = {"username": request.form.get('username'),
                     "password": request.form.get('password'),
                     "email": request.form.get('email')}

        # Verify user data is as expected
        verify_data = Verify.verify_user_details(user_data)
        if not verify_data["success"]:
            return verify_data["errors"], 400

        # Check user logged in or exists
        if Verify.verify_user(user_data["username"],
                              user_data["password"],
                              ):
            return {"message": "You are already logged in or user exists"}, 403

        # User passed register him/her
        new_user = User(user_data["username"],
                        user_data["email"],
                        user_data["password"])
        self.add_to_db(new_user)

        # Make new return dict since popping password affects
        # original dict affecting tests
        response = {"username": user_data["username"],
                    "email": user_data["email"]}
        return response, 201


class UserBucketlists(Resource, Common):
    """Bundles all processes from the request
       /bucketlists
    """
    @auth.login_required
    def post(self):
        """Creates a new bucketlist"""
        bucketlist_data = {"name": request.form.get("name")}

        # Validate bucketlist data
        verify_data = Verify.verify_bucketlist_details(bucketlist_data)
        if not verify_data["success"]:
            return verify_data["errors"], 400

        # Check if bucketlist exists
        bucketlist = Verify.verify_bucketlist_exists(bucketlist_name=bucketlist_data["name"].lower())
        if bucketlist:
            return {"name": "The bucketlist '{}' already exists".format(bucketlist_data["name"])}, 400

        # Create bucketlist
        new_bucketlist = Bucketlists(bucketlist_data["name"],
                                     g.user.id)
        self.add_to_db(new_bucketlist)

        response = {"bucketlist": bucketlist_data["name"]}
        return response, 201

    @auth.login_required
    def get(self):
        """Retreives all bucketlists"""
        # Get all bucketlists
        bucketlists = Bucketlists.query.filter_by(created_by=g.user.id)
        response = []

        for bucketlist in bucketlists:
            result, errors = bucketlist_schema.dump(bucketlist)
            response.append(result)

        return response, 200



class SingleBucketlist(Resource, Common):
    """Bundles all processes from the request
       /bucketlists/<id>
    """
    @auth.login_required
    def get(self, id):
        """Retreives a single bucketlist and items"""
        # Verify bucketlist exists
        bucketlist = Verify.verify_bucketlist_exists(bucketlist_id=id)
        if not bucketlist:
            return {"message": "Bucketlist does not exist"}, 404

        response, errors = bucketlist_schema.dump(bucketlist)

        return response, 200

    @auth.login_required
    def put(self, id):
        """Updates a single bucketlist"""
        bucketlist_data = {"name": request.form.get("name")}

        # Validate bucketlist data
        verify_data = Verify.verify_bucketlist_details(bucketlist_data)
        if not verify_data["success"]:
            return verify_data["errors"], 400

        # Verify bucketlist exists
        bucketlist = Verify.verify_bucketlist_exists(bucketlist_id=id)
        if not bucketlist:
            return {"message": "Bucketlist does not exist"}, 404

        # Change data
        bucketlist.name = bucketlist_data["name"]
        bucketlist.update_date_modified()
        self.update_db()

        response, errors = bucketlist_schema.dump(bucketlist)

        return response, 200

    @auth.login_required
    def delete(self, id):
        """Deletes a bucketlist"""
        # Verify bucketlist exists
        bucketlist = Verify.verify_bucketlist_exists(bucketlist_id=id)
        if not bucketlist:
            return {"message": "Bucketlist does not exist"}, 404

        # Delete items associated with bucketlist
        bucketlist_items = Items.query.filter_by(bucketlist=bucketlist.id)
        for item in bucketlist_items:
            self.delete_db_record(item)

        # Delete bucketlist
        self.delete_db_record(bucketlist)

        return {"message": "Bucketlist successfully deleted"}, 200


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

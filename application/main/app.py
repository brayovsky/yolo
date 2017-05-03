from urllib.parse import urljoin

from flask import Flask, request, g, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
# Load configurations
app.config.from_object("application.settings.DevelopmentConfig")

# Ignore pep8 to enable cyclic import
from application.models.models import User, Bucketlists, Items, db
from application.main.verify import Verify, BucketListSchema, ItemsSchema, auth

api = Api(app, prefix="/api/v1")
bucketlist_schema = BucketListSchema()
item_schema = ItemsSchema()


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

    @staticmethod
    def get_int_or_default(val, default):
        """Used to get an int or default to a value"""
        if type(default) is not int:
            raise ValueError("Default value must be an integer")

        try:
            intval = int(val)
        except ValueError:
            # If val say is an inconvertible string
            intval = default
        except TypeError:
            # If val is none
            intval = default

        return intval


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
            return {"authenticated": False}, 401

        return {"user": user.username,
                "token": user.token,
                "authenticated": True}, 200


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

        # Check user exists
        if Verify.check_username_exists(user_data["username"]):
            return {"message": "User exists"}, 403

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
        try:
            bucketlist = Verify.verify_bucketlist_exists(
                bucketlist_name=bucketlist_data["name"].lower())
        except TypeError:
            # Bucketlist name was an empty string
            return {"name": ["Field may not be null."]}, 400

        if bucketlist:
            return {"name": "The bucketlist '{}' already exists"
                    .format(bucketlist_data["name"])},\
                400

        # Create bucketlist
        new_bucketlist = Bucketlists(bucketlist_data["name"],
                                     g.user.id)
        self.add_to_db(new_bucketlist)
        # Get created bucketlist from database
        new_bucketlist = Bucketlists.query.filter_by(
            name=bucketlist_data["name"].lower(),
            created_by=g.user.id).first()

        response, errors = bucketlist_schema.dump(new_bucketlist)
        return response, 201

    @auth.login_required
    def get(self):
        """Retreives all bucketlists"""
        # Get page and limit, default is 1 and 20 respectively
        page = self.get_int_or_default(request.args.get("page"), 1)
        limit = self.get_int_or_default(request.args.get("limit"), 20)
        search_string = request.args.get("q") or False

        next_url = None
        prev_url = None
        site_root = app.config["SITE_ROOT"]

        # Get all paginated bucketlists
        if search_string:
            # Search
            bucketlists = Bucketlists.query.filter_by(
                created_by=g.user.id).search(search_string).paginate(
                page=page,
                per_page=limit)
        else:
            # Get all bucketlists
            bucketlists = Bucketlists.query.filter_by(
                created_by=g.user.id).paginate(page=page, per_page=limit)

        if bucketlists.has_next:
            next_url = urljoin(
                site_root, api.url_for(UserBucketlists,
                                       page=bucketlists.next_num,
                                       limit=bucketlists.per_page))
        if bucketlists.has_prev:
            prev_url = urljoin(
                site_root, api.url_for(UserBucketlists,
                                       page=bucketlists.prev_num,
                                       limit=bucketlists.per_page))

        response = {"number": bucketlists.total,
                    "limit": bucketlists.per_page,
                    "current_page": bucketlists.page,
                    "pages": bucketlists.pages,
                    "prev": prev_url,
                    "next": next_url,
                    "bucketlists": []}

        for bucketlist in bucketlists.items:
            result, errors = bucketlist_schema.dump(bucketlist)
            response["bucketlists"].append(result)

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

        return response, 201

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
        item_data = {"name": request.form.get("name")}
        # Verify item data
        item_valid = Verify.verify_item_details(item_data)
        if not item_valid["success"]:
            return item_valid["errors"], 400

        # Verify bucketlist exists
        bucketlist = Verify.verify_bucketlist_exists(bucketlist_id=id)
        if not bucketlist:
            return {"message": "Bucketlist does not exist"}, 404

        # Verify name is not a duplicate
        item_exists = Verify.verify_item_exists(id,
                                                item_name=item_data["name"])
        if item_exists:
            return {"message": "This item already exists in the bucketlist"},\
                400

        # Save item
        item = Items(item_data["name"], bucketlist.id)
        self.add_to_db(item)

        # Get new item
        item = Items.query.filter_by(name=item_data["name"].lower(),
                                     bucketlist=bucketlist.id).first()
        item_return, error = item_schema.dump(item)

        return item_return, 201


class BucketListItems(Resource, Common):
    """Bundles all processes from the request
       /bucketlists/<id>/items/<item_id>
    """
    @auth.login_required
    def put(self, id, item_id):
        """Updates an item in a bucketlist"""
        item_data = {"name": request.form.get("name")}

        # Verify if data is valid
        item_data_valid = Verify.verify_item_details(item_data)
        if not item_data_valid["success"]:
            return item_data_valid["errors"], 400

        # Verify bucketlist exists
        bucketlist_exists = Verify.verify_bucketlist_exists(
            bucketlist_id=id
        )

        if not bucketlist_exists:
            return {"message": "Bucketlist does not exist"}, 404

        # Verify item exists
        item = Verify.verify_item_exists(id, item_id=item_id)
        if not item:
            return {"message": "Item does not exist"}, 404

        # Update name
        item.name = item_data["name"]
        item.update_date_modified()
        self.update_db()

        # Get new item
        item = Items.query.filter_by(name=item_data["name"],
                                     bucketlist=id).first()
        item_return, error = item_schema.dump(item)

        return item_return, 201

    @auth.login_required
    def delete(self, id, item_id):
        """Deletes an item in a bucketlist"""
        # Verify bucketlist exists
        bucketlist_exists = Verify.verify_bucketlist_exists(
            bucketlist_id=id
        )

        if not bucketlist_exists:
            return {"message": "Bucketlist does not exist"}, 404

        # Verify item exists
        item = Verify.verify_item_exists(id, item_id=item_id)
        if not item:
            return {"message": "Item does not exist"}, 404

        # Delete item
        self.delete_db_record(item)
        return {"message": "Item successfully deleted"}, 200


api.add_resource(Login, "/auth/login/", strict_slashes=False)
api.add_resource(Register, "/auth/register/", strict_slashes=False)
api.add_resource(UserBucketlists, "/bucketlists/", strict_slashes=False)
api.add_resource(SingleBucketlist, "/bucketlists/<id>/", strict_slashes=False)
api.add_resource(NewBucketListItems, "/bucketlists/<id>/items/",
                 strict_slashes=False)
api.add_resource(BucketListItems, "/bucketlists/<id>/items/<item_id>/",
                 strict_slashes=False)


# Normal html response routes
@app.route("/")
def show_skeleton():
    return render_template("home.html")

@app.route("/partials/main.html")
def show_landingpage():
    return render_template("partials/landingpage.html")


if __name__ == "__main__":
    app.run()

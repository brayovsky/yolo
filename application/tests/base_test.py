from unittest import TestCase
from base64 import b64encode

from application.main.app import User, Bucketlists, Items, db, app


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        app.config.from_object("application.settings.TestingConfig")
        self.app = app.app_context().push()
        self.client = app.test_client()
        db.create_all()

        # Set a user Bob
        self.bob = User("Bob", "bob@email.com", "password")
        db.session.add(self.bob)
        db.session.commit()

        self.bob = User.query.filter_by(username="bob").first()
        self.bob.raw_password = "password"

        # Add a bucketlist to Bob
        self.bucketlist = Bucketlists("bucketlist1", self.bob.id)

        db.session.add(self.bucketlist)
        db.session.commit()
        self.bucketlist = Bucketlists.query.filter_by(
            name="bucketlist1").first()

        # Add items to Bob's bucketlists
        self.item = Items("item1", self.bucketlist.id)

        db.session.add(self.item)
        db.session.commit()
        self.item = Items.query.filter_by(name="item1").first()

        self.authorization = self.get_authorisation_header()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        db.session.remove()
        db.drop_all()

    def get_authorisation_header(self):
        auth_string = self.bob.username + ":" + self.bob.raw_password
        header = "Basic " + b64encode(auth_string.encode()).decode()
        return header

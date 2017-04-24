from unittest import TestCase
from base64 import b64encode

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from application.main.app import User, Bucketlists, Items, db, app


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        app.config.from_object("application.default_settings.TestingConfig")
        app.config.from_envvar("YOLO_SETTINGS")
        self.app = app.app_context().push()
        self.client = app.test_client()
        db.create_all()

        # Set a user Bob
        self.bob = User("Bob", "bob@email.com", "password")
        db.session.add(self.bob)
        db.session.commit()

        self.bob = User.query.filter_by(username="Bob").first()
        self.bob.raw_password = "password"

        # Add a bucketlist to Bob
        self.bucketlist = Bucketlists("bucketlist1", self.bob.id)

        db.session.add(self.bucketlist)
        db.session.commit()
        self.bucketlist = Bucketlists.query.filter_by(name="bucketlist1").first()

        # Add items to Bob's bucketlists
        self.item = Items("item1", self.bucketlist.id)

        db.session.add(self.item)
        db.session.commit()
        self.item = Items.query.filter_by(name="item1").first()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        db.session.remove()
        db.drop_all()

    def get_authorisation_header(self):
        # Log in bob
        # acqujre token and base 64 encode it.
        # set the encoded token in authorisation header
        s = Serializer(app.config['SECRET_KEY'], expires_in=600)
        token = s.dumps({'id': self.bob.id})

        # decode from bytes to string
        header = "Basic " + b64encode(token).decode()
        return header


from unittest import TestCase

from application.main.app import User, Bucketlists, Items, app


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

        # Set a user Bob
        self.bob = User("Bob", "bob@email.com", "password")

        # Add a bucketlist to Bob
        self.bucketlist = Bucketlists("bucketlist1", self.bob)

        # Add items to Bob's bucketlists
        self.item = Items("item1", self.bucketlist)

        # Save bob and make a user instance of him for tests
        # that need his details

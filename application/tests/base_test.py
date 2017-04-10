from unittest import TestCase

from application.models.models import User, Bucketlists, Items


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

    # Set a user Bob
    self.bob = User("Bob", "bob@email.com", "password")

    # Add a bucketlist to Bob


    # Add items to Bob's bucketlists


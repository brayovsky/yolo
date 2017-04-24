import unittest
from unittest.mock import patch

from application.tests.base_test import BaseTestCase


class TestCreateBucketlist(BaseTestCase):
    """Tests endpoint for creating bucketlists"""
    def setUp(self):
        super(TestCreateBucketlist, self).setUp()
        self.url = "/v1/bucketlists"

    def test_create_bucketlist_validates_data(self):
        pass

    def test_create_bucketlist_rejects_similar_name(self):

        pass

    def test_creates_bucketlist_with_valid_parameters(self):
        # Adds to database
        # Return status is 201
        pass


class TestRetrieveBucketlists(BaseTestCase):
    """Tests endpoint for retreiving bucketlists"""
    pass


if __name__ == '__main__':
    unittest.main()

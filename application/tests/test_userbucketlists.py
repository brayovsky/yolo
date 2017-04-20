import unittest

from application.tests.base_test import BaseTestCase


class TestBucketlists(BaseTestCase):
    def test_cannot_create_when_logged_out(self):
        pass

    def test_cannot_retreive_when_logged_out(self):
        pass

    def test_retreives_bucketlists(self):
        pass

    def test_creates_bucketlists(self):
        pass

    def test_does_not_create_bucketlists_with_same_name(self):
        pass

    def test_creates_bucketlists_using_post(self):
        pass

    def test_retreives_bucketlists_using_get(self):
        pass


if __name__ == '__main__':
    unittest.main()
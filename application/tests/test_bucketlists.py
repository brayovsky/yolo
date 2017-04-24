import unittest
from unittest.mock import patch
import json

from application.tests.base_test import BaseTestCase, db, Bucketlists


class TestCreateBucketlist(BaseTestCase):
    """Tests endpoint for creating bucketlists"""
    def setUp(self):
        super(TestCreateBucketlist, self).setUp()
        self.url = "/v1/bucketlists"
        self.bucketlist_data = {"name": "before 26"}
        self.authorization = self.get_authorisation_header()

    def test_create_bucketlist_validates_data(self):
        # Function responsible for validating bucketlist data
        # is verify_bucketlist_data
        # Assert it is called with the correct parameters
        with patch("application.main.verify.Verify.verify_bucketlist_details",
                   return_value={"success": True}) as verify_bucketlist_data:
            self.client.post(self.url,
                             data=self.bucketlist_data,
                             headers={"Authorization": self.authorization})

            verify_bucketlist_data.assert_called_with(self.bucketlist_data)

    def test_create_bucketlist_checks_similar_name(self):
        # Function responsible for checking similar names
        # is verify_bucketlist_exists
        # Assert it is called with the correct parameters
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value={"success": True}) as verify_bucketlist_exists:
            self.client.post(self.url,
                             data=self.bucketlist_data,
                             headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_name=self.bucketlist_data["name"])

    def test_creates_bucketlist_with_valid_parameters(self):
        # Adds to database
        # Return status is 201
        with patch("application.main.app.Common.add_to_db") as add_to_database:
            request = self.client.post(self.url,
                                       data=self.bucketlist_data,
                                       headers={
                                           "Authorization": self.authorization}
                                       )
            add_to_database.assert_called_once()

            assert request.status_code == 201

    def test_create_bucketlist_api_return(self):
        request = self.client.post(self.url,
                                   data=self.bucketlist_data,
                                   headers={
                                       "Authorization": self.authorization})

        expected_response = {"bucketlist": self.bucketlist_data["name"]}
        response = json.loads(request.data)

        self.assertDictEqual(expected_response,
                             response)


class TestRetrieveBucketlists(BaseTestCase):
    """Tests endpoint for retrieving bucketlists"""
    def setUp(self):
        super(TestRetrieveBucketlists, self).setUp()
        self.url = "/v1/bucketlists"
        self.authorization = self.get_authorisation_header()

    def test_retrieve_gets_users_bucketlists_only(self):
        # Add Bucketlist
        new_bucketlist = Bucketlists("at 60", 2)
        db.session.add(new_bucketlist)
        db.session.commit()
        request = self.client.get(self.url,
                                  headers={
                                      "Authorization": self.authorization})
        bucketlists = json.loads(request.data)

        for bucketlist in bucketlists:
            assert bucketlist["created_by"] == self.bob.id


if __name__ == '__main__':
    unittest.main()

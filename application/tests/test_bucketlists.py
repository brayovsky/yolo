import unittest
from unittest.mock import patch
import json

from application.tests.base_test import BaseTestCase, db, Bucketlists, User


class TestCreateBucketlist(BaseTestCase):
    """Tests endpoint for creating bucketlists"""
    def setUp(self):
        super(TestCreateBucketlist, self).setUp()
        self.url = "api/v1/bucketlists/"
        self.bucketlist_data = {"name": "before 26"}
        self.authorization = self.get_authorisation_header()

    def test_post_bucketlist_validates_data(self):
        # Function responsible for validating bucketlist data
        # is verify_bucketlist_data
        # Assert it is called with the correct parameters
        with patch("application.main.verify.Verify.verify_bucketlist_details",
                   return_value={"success": True}) as verify_bucketlist_data:
            self.client.post(self.url,
                             data=self.bucketlist_data,
                             headers={"Authorization": self.authorization})

            verify_bucketlist_data.assert_called_with(self.bucketlist_data)

    def test_post_bucketlist_checks_similar_name(self):
        # Function responsible for checking similar names
        # is verify_bucketlist_exists
        # Assert it is called with the correct parameters
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=True) as verify_bucketlist_exists:
            self.client.post(self.url,
                             data=self.bucketlist_data,
                             headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_name=self.bucketlist_data["name"])

    def test_post_bucketlist_with_valid_parameters(self):
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

    def test_post_bucketlist_api_return(self):
        request = self.client.post(self.url,
                                   data=self.bucketlist_data,
                                   headers={
                                       "Authorization": self.authorization})

        assert request.status_code == 201


class TestRetrieveBucketlists(BaseTestCase):
    """Tests endpoint for retrieving all bucketlists"""
    def setUp(self):
        super(TestRetrieveBucketlists, self).setUp()
        self.url = "api/v1/bucketlists/"
        self.authorization = self.get_authorisation_header()

    def test_get_gets_users_bucketlists_only(self):
        # Add Bucketlist
        new_bucketlist = Bucketlists("at 60", 2)
        db.session.add(new_bucketlist)
        db.session.commit()
        request = self.client.get(self.url,
                                  headers={
                                      "Authorization": self.authorization})
        bucketlists = json.loads(request.data)["bucketlists"]

        for bucketlist in bucketlists:
            assert bucketlist["created_by"] == self.bob.id


class TestRetrieveSingleBucketlist(BaseTestCase):
    """Test endpoint for retreiving single bucketlist"""
    def setUp(self):
        super(TestRetrieveSingleBucketlist, self).setUp()
        self.url_prefix = "api/v1/bucketlists/"
        self.authorization = self.get_authorisation_header()

    def test_get_checks_if_bucketlist_exists(self):
        # Function verify_bucketlist_exists() checks if
        # bucketlist exists
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=False) as verify_bucketlist_exists:
            bucketlist_id = str(self.bucketlist.id)
            self.client.get(self.url_prefix + bucketlist_id + "/",
                            headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_id=bucketlist_id)

    def test_get_gets_users_bucketlists_only(self):
        # Make an bucketlist id that does not belong to the user bob and
        # try to request it
        alice = User("Alice", "alice@email.com", "password")
        db.session.add(alice)
        db.session.commit()
        alice = User.query.filter_by(username="alice").first()
        # Add a bucketlist to Alice
        alice_bucketlist = Bucketlists("bucketlist2", alice.id)
        db.session.add(alice_bucketlist)
        db.session.commit()
        alice_bucketlist = Bucketlists.query.filter_by(
            name="bucketlist2").first()
        bucketlist_id = str(alice_bucketlist.id)

        # Get alice's bucketlist with bob's authorization
        request = self.client.get(self.url_prefix + bucketlist_id + "/",
                                  headers={"Authorization": self.authorization}
                                  )
        assert request.status_code == 404

    def test_get_api_response_with_wrong_parameters(self):
        # Send a bucketlist id that does not exist
        request = self.client.get(self.url_prefix + "4000" + "/",
                                  headers={"Authorization": self.authorization}
                                  )
        # Decode json data
        response = json.loads(request.data)
        expected_response = {"message": "Bucketlist does not exist"}

        self.assertDictEqual(response, expected_response)

    def test_get_api_response_with_valid_parameters(self):
        bucketlist_id = str(self.bucketlist.id)
        request = self.client.get(self.url_prefix + bucketlist_id + "/",
                                  headers={"Authorization": self.authorization}
                                  )

        assert request.status_code == 200


class TestUpdateSingleBucketlist(BaseTestCase):
    def setUp(self):
        super(TestUpdateSingleBucketlist, self).setUp()
        self.url_prefix = "api/v1/bucketlists/"
        self.authorization = self.get_authorisation_header()
        self.bucketlist_data = {"name": "new name"}

    def test_put_validates_bucketlist_data(self):
        # check if verify_bucketlist_data was called
        with patch("application.main.verify.Verify.verify_bucketlist_details",
                   return_value={"success": True}) as verify_bucketlist_data:
            self.client.put(self.url_prefix + "4000" + "/",
                            data=self.bucketlist_data,
                            headers={"Authorization": self.authorization})

            verify_bucketlist_data.assert_called_with(self.bucketlist_data)

    def test_put_verifies_bucketlist_exists(self):
        # Check if verify_bucketlist_exists was called
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=False) as verify_bucketlist_exists:
            bucketlist_id = str(self.bucketlist.id)
            self.client.put(self.url_prefix + bucketlist_id + "/",
                            data=self.bucketlist_data,
                            headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_id=bucketlist_id)

    def test_api_with_missing_data(self):
        # Test without sending name
        request = self.client.put(
            self.url_prefix + str(self.bucketlist.id) + "/",
            headers={"Authorization": self.authorization})

        assert request.status_code == 400

    def test_api_with_correct_data(self):
        # Test when sending the correct name
        request = self.client.put(
            self.url_prefix + str(self.bucketlist.id) + "/",
            data=self.bucketlist_data,
            headers={"Authorization": self.authorization})

        assert request.status_code == 200


class TestDeleteSingleBucketlist(BaseTestCase):
    def setUp(self):
        super(TestDeleteSingleBucketlist, self).setUp()
        self.url_prefix = "api/v1/bucketlists/"
        self.authorization = self.get_authorisation_header()

    def test_delete_verifies_bucketlist_exists(self):
        # Check verify bucketlist was called
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=False) as verify_bucketlist_exists:
            self.client.delete(self.url_prefix + "4000" + "/",
                               headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(bucketlist_id="4000")

    def test_delete_api_with_wrong_data(self):
        # Use a non existent id '4000'
        request = self.client.delete(
            self.url_prefix + "4000" + "/",
            headers={"Authorization": self.authorization})

        request_response = json.loads(request.data)
        expected_response = {"message": "Bucketlist does not exist"}

        self.assertDictEqual(request_response, expected_response)

    def test_delete_api_with_correct_data(self):
        # Use bucketlist created by Bob
        request = self.client.delete(
            self.url_prefix + str(self.bucketlist.id) + "/",
            headers={"Authorization": self.authorization})

        request_response = json.loads(request.data)
        expected_response = {"message": "Bucketlist successfully deleted"}

        self.assertDictEqual(request_response, expected_response)


if __name__ == '__main__':
    unittest.main()

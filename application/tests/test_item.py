import unittest
from unittest.mock import patch
import json

from application.tests.base_test import BaseTestCase


class TestCreateNewItem(BaseTestCase):
    def setUp(self):
        super(TestCreateNewItem, self).setUp()
        self.url = "api/v1/bucketlists/" + str(self.bucketlist.id) + "/items/"
        self.item_data = {"name": "new_name"}

    def test_post_validates_data(self):
        # Check if verify_item_details was called
        with patch("application.main.verify.Verify.verify_item_details",
                   return_value={"success": True}) as verify_item_details:
            self.client.post(self.url,
                             data=self.item_data,
                             headers={"Authorization": self.authorization})

            verify_item_details.assert_called_with(
                self.item_data)

    def test_post_checks_for_duplicate_data(self):
        # Check if verify_item_exists was called
        with patch("application.main.verify.Verify.verify_item_exists",
                   return_value=False) as verify_item_exists:
            self.client.post(self.url,
                             data=self.item_data,
                             headers={"Authorization": self.authorization})

            verify_item_exists.assert_called_with(
                str(self.bucketlist.id), item_name=self.item_data["name"])

    def test_post_checks_if_bucketlist_exists(self):
        # Check if verify_bucketlist_exists was called
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=False) as verify_bucketlist_exists:
            self.client.post(self.url,
                             data=self.item_data,
                             headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_id=str(self.bucketlist.id)
            )

    def test_post_api_with_duplicate_item(self):
        # Use self.item as the existing item
        request = self.client.post(self.url,
                                   data={"name": self.item.name},
                                   headers={"Authorization": self.authorization
                                            }
                                   )
        request_response = json.loads(request.data)
        expected_response = {
            "message": "This item already exists in the bucketlist"}
        self.assertDictEqual(request_response, expected_response)

    def test_post_api_with_non_existent_bucketlist(self):
        # Use bucketlist id '4000'
        request = self.client.post("api/v1/bucketlists/4000/items/",
                                   data={"name": self.item.name},
                                   headers={"Authorization": self.authorization
                                            }
                                   )
        request_response = json.loads(request.data)
        expected_response = {"message": "Bucketlist does not exist"}
        self.assertDictEqual(request_response, expected_response)

    def test_post_api_with_correct_data(self):
        # Use self.bucketlist and self.item_data
        request = self.client.post(self.url,
                                   data=self.item_data,
                                   headers={"Authorization": self.authorization
                                            }
                                   )

        assert request.status_code == 201


class TestEditItem(BaseTestCase):
    def setUp(self):
        super(TestEditItem, self).setUp()
        self.url = "api/v1/bucketlists/" + str(self.bucketlist.id) + \
                   "/items/" + str(self.item.id) + "/"
        self.item_data = {"name": "updated name"}

    def test_put_verifies_data_sent(self):
        # Check if verify_item_details was called
        with patch("application.main.verify.Verify.verify_item_details",
                   return_value={"success": True}) as verify_item_details:
            self.client.put(self.url,
                            data=self.item_data,
                            headers={"Authorization": self.authorization})

            verify_item_details.assert_called_with(
                self.item_data)

    def test_put_checks_bucketlist_exists(self):
        # Check if verify_bucketlist_exists was called
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=False) as verify_bucketlist_exists:
            self.client.put(self.url,
                            data=self.item_data,
                            headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_id=str(self.bucketlist.id))

    def test_put_checks_item_exists(self):
        # Check if verify_item_exists was called
        with patch("application.main.verify.Verify.verify_item_exists",
                   return_value=False) as verify_item_exists:
            self.client.put(self.url,
                            data=self.item_data,
                            headers={"Authorization": self.authorization})

            verify_item_exists.assert_called_with(
                str(self.bucketlist.id), item_id=str(self.item.id))

    def test_put_api_with_missing_data(self):
        request = self.client.put(self.url,
                                  headers={"Authorization": self.authorization}
                                  )

        assert request.status_code == 400

    def test_put_api_with_invalid_bucketlist(self):
        # Use non existent bucketlist id '4000'
        request = self.client.put("api/v1/bucketlists/4000/items/1/",
                                  data=self.item_data,
                                  headers={"Authorization": self.authorization}
                                  )
        request_response = json.loads(request.data)
        expexted_response = {"message": "Bucketlist does not exist"}

        self.assertDictEqual(request_response, expexted_response)

    def test_put_api_with_invalid_item(self):
        # Use non existent item id '4000'
        request = self.client.put(
            "api/v1/bucketlists/" + str(self.bucketlist.id) + "/items/4000/",
            data=self.item_data,
            headers={"Authorization": self.authorization})

        request_response = json.loads(request.data)
        expexted_response = {"message": "Item does not exist"}

        self.assertDictEqual(request_response, expexted_response)

    def test_put_api_with_valid_data(self):
        request = self.client.put(
            self.url,
            data=self.item_data,
            headers={"Authorization": self.authorization})

        assert request.status_code == 200


class TestDeleteItem(BaseTestCase):
    def setUp(self):
        super(TestDeleteItem, self).setUp()
        self.url = "api/v1/bucketlists/" + str(self.bucketlist.id) + \
                   "/items/" + str(self.item.id) + "/"

    def test_delete_checks_bucketlist_exists(self):
        # Check if verify_bucketlist_exists was called
        with patch("application.main.verify.Verify.verify_bucketlist_exists",
                   return_value=False) as verify_bucketlist_exists:
            self.client.delete(self.url,
                               headers={"Authorization": self.authorization})

            verify_bucketlist_exists.assert_called_with(
                bucketlist_id=str(self.bucketlist.id))

    def test_delete_checks_item_exists(self):
        # Check if verify_item_exists was called
        with patch("application.main.verify.Verify.verify_item_exists",
                   return_value=False) as verify_item_exists:
            self.client.delete(self.url,
                               headers={"Authorization": self.authorization})

            verify_item_exists.assert_called_with(
                str(self.bucketlist.id), item_id=str(self.item.id))

    def test_delete_api_with_invalid_bucketlist(self):
        # Use non existent bucketlist id '4000'
        request = self.client.delete(
            "api/v1/bucketlists/4000/items/" + str(self.item.id) + "/",
            headers={"Authorization": self.authorization})
        request_response = json.loads(request.data)
        expexted_response = {"message": "Bucketlist does not exist"}

        self.assertDictEqual(request_response, expexted_response)

    def test_delete_api_with_invalid_item(self):
        # Use non existent item id '4000'
        request = self.client.delete(
            "api/v1/bucketlists/" + str(self.bucketlist.id) + "/items/4000/",
            headers={"Authorization": self.authorization})

        request_response = json.loads(request.data)
        expexted_response = {"message": "Item does not exist"}

        self.assertDictEqual(request_response, expexted_response)

    def test_delete_api_with_valid_data(self):
        request = self.client.delete(
            self.url,
            headers={"Authorization": self.authorization})

        assert request.status_code == 200

if __name__ == '__main__':
    unittest.main()

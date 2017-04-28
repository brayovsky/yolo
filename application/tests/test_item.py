import unittest
from unittest.mock import patch
import json

from application.tests.base_test import BaseTestCase


class TestCreateNewItem(BaseTestCase):
    def setUp(self):
        super(TestCreateNewItem, self).setUp()
        self.url = "/v1/bucketlists/" + str(self.bucketlist.id) + "/items"
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
        expected_response = {"message": "This item already exists in the bucketlist"}
        self.assertDictEqual(request_response, expected_response)

    def test_post_api_with_non_existent_bucketlist(self):
        # Use bucketlist id '4000'
        request = self.client.post("/v1/bucketlists/4000/items",
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


if __name__ == '__main__':
    unittest.main()

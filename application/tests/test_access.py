import unittest
from unittest.mock import MagicMock
import json

from application.tests.base_test import BaseTestCase
from application.main.verify import Verify


class TestRegister(BaseTestCase):
    def setUp(self):
        super(TestRegister, self).setUp()
        self.user_data = {"username": "baba",
                          "password": "cheers",
                          "email": "cheers@baba.com"}

    def test_register_validates_data(self):
        # Function verify_user_data validates user data
        # Check if verify_user_data was called

        Verify.verify_user_details = MagicMock()
        self.client.post("/v1/auth/register",
                                    data=self.user_data)

        Verify.verify_user_details.assert_called_with(self.user_data)

    def test_register_checks_user_exists(self):
        # Function verify_user will check if user exists
        # Assert verify_user was called

        Verify.verify_user = MagicMock()
        self.client.post("/v1/auth/register",
                                    data=self.user_data)

        Verify.verify_user.assert_called_with(self.user_data["username"],
                                              self.user_data["password"])

    def test_register_api_status_with_valid_data(self):
        # Check status code
        response = self.client.post("/v1/auth/register",
                                    data=self.user_data)

        assert response.status_code == 201

    def test_register_api_response_with_valid_data(self):
        # Check response
        response = self.client.post("/v1/auth/register",
                                    data=self.user_data)
        expected_response = {"username": self.user_data["username"],
                             "email": self.user_data["email"]}

        reg_response = json.loads(response.data)
        self.assertDictEqual(reg_response,
                             expected_response)


class TestLogIn(BaseTestCase):
    def test_does_not_login_invalid_user(self):
        pass

    def test_logs_in_with_post_only(self):
        pass

if __name__ == "__main__":
    unittest.main()

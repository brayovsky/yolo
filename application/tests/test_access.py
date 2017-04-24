import unittest
from unittest.mock import MagicMock, patch
import json

from application.tests.base_test import BaseTestCase, User
from application.main.verify import Verify


class TestRegister(BaseTestCase):
    def setUp(self):
        super(TestRegister, self).setUp()
        self.user_data = {"username": "baba",
                          "password": "cheers",
                          "email": "cheers@baba.com"}
        self.url = "/v1/auth/register"

    def test_register_validates_data(self):
        # Function verify_user_data validates user data
        # Check if verify_user_data was called

        with patch('application.main.verify.Verify.verify_user_details',
                   return_value={"success": True}) as verify_user_details:
            self.client.post(self.url,
                             data=self.user_data)

            verify_user_details.assert_called_with(self.user_data)

    def test_register_checks_user_exists(self):
        # Function verify_user will check if user exists
        # Assert verify_user was called

        with patch('application.main.verify.Verify.verify_user',
                   return_value=False) as verify_user:
            self.client.post(self.url,
                             data=self.user_data)

            verify_user.assert_called_with(self.user_data["username"],
                                           self.user_data["password"])

    def test_register_api_status_with_valid_data(self):
        # Check status code
        response = self.client.post(self.url,
                                    data=self.user_data)

        assert response.status_code == 201

    def test_register_api_response_with_valid_data(self):
        # Check response
        response = self.client.post(self.url,
                                    data=self.user_data)
        expected_response = {"username": self.user_data["username"],
                             "email": self.user_data["email"]}

        reg_response = json.loads(response.data)
        self.assertDictEqual(reg_response,
                             expected_response)


class TestLogIn(BaseTestCase):
    def setUp(self):
        super(TestLogIn, self).setUp()
        self.user_data = {"username": "baba",
                          "password": "cheers"}
        self.url = "/v1/auth/login"

    def test_login_validates_data(self):
        # Function verify_user_data validates user data
        # Check if verify_user_data was called

        with patch('application.main.verify.Verify.verify_user_details',
                   return_value={"success": True}) as verify_user_details:
            self.client.post(self.url,
                             data=self.user_data)

            verify_user_details.assert_called_with(self.user_data)

    def test_login_checks_user_exists(self):
        # Function verify_login will check if user exists and log in
        # Assert verify_user was called

        with patch('application.main.verify.Verify.verify_login',
                   return_value=self.bob) as verify_login_mock:
            # Assign User object a token to prevent raising an
            # AttributeError in the main code
            self.bob.token = "randomstring"
            self.client.post(self.url,
                             data=self.user_data)

            verify_login_mock.assert_called_with(self.user_data["username"],
                                                   self.user_data["password"])

    def test_login_status_with_valid_credentials(self):
        user_data = {"username": self.bob.username,
                     "password": self.bob.raw_password}
        response = self.client.post(self.url,
                                    data=user_data)

        assert response.status_code == 200

    def test_login_status_with_invalid_credentials(self):
        users_data = {"username": "fdghgkjk",
                      "password": "jhjk"}
        response = self.client.post(self.url,
                                    data=users_data)

        assert response.status_code == 401


if __name__ == "__main__":
    unittest.main()

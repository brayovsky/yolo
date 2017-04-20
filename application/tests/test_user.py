import unittest
from unittest.mock import MagicMock

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from application.tests.base_test import BaseTestCase, User, app


class TestUserModel(BaseTestCase):
    def test_hashes_password(self):
        # Since hash is unpredictable, test if original
        # password is not equal to new password_hash and
        # password hash is longer than original password
        raw_password = "password"
        password_hash = self.bob.hash_password("password")

        assert raw_password != password_hash and \
            len(raw_password) < len(password_hash)

    def test_verifies_valid_password(self):
        # Bob's password is password
        assert self.bob.verify_password("password")

    def test_does_not_verify_invalid_password(self):
        assert not self.bob.verify_password("invalid_password")

    def test_generates_auth_token(self):
        # Assert dumps method of serializer is called
        # with a dictionary of the user id
        s = Serializer(app.config['SECRET_KEY'], expires_in=600)
        s.dumps = MagicMock()
        self.bob.generate_auth_token(expiration=600)
        s.dumps.assert_called_with({'id': self.bob.id})

    def test_does_not_verify_invalid_token(self):
        assert not User.verify_auth_token("invalidtoken")


if __name__ == '__main__':
    unittest.main()
from application.tests.base_test import BaseTestCase


class TestUserModel(BaseTestCase):
    def setUp(self):
        super(TestUserModel, self).setUp()

    def tearDown(self):
        pass

    def test_hashes_password(self):
        pass

    def test_verifies_valid_password(self):
        pass

    def test_does_not_verify_valid_password(self):
        pass

    def test_generates_auth_token(self):
        pass

    def test_does_not_verify_invalid_token(self):
        pass

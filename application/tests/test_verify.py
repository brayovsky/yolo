from application.main.verify import Verify
from application.tests.base_test import BaseTestCase


class TestVerify(BaseTestCase):
    def setUp(self):
        super(TestVerify, self).setUp()

    def tearDown(self):
        pass

    def test_verify_id_is_int_with_string(self):
        pass

    def test_verify_id_is_int_with_int(self):
        pass

    def test_verify_bucketlist_exists_with_invalid_bucketlist(self):
        pass

    def test_verify_bucketlist_exists_with_valid_bucketlist(self):
        pass

    def test_verify_item_exists_with_invalid_item(self):
        pass

    def test_verify_item_exists_with_valid_item(self):
        pass

    def test_verify_password_with_invalid_password(self):
        pass

    def test_verify_password_with_valid_password(self):
        pass

    def test_verify_username_with_invalid_username(self):
        pass

    def test_verify_username_with_valid_username(self):
        pass

    def test_user_exists_with_invalid_email(self):
        pass

    def test_user_exists_with_valid_email_and_username(self):
        pass

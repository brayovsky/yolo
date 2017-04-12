from application.main.verify import Verify
from application.tests.base_test import BaseTestCase


class TestVerify(BaseTestCase):
    def setUp(self):
        super(TestVerify, self).setUp()
        # Set huge number for an impossible id
        self.invalid_bucketlist_id = 4000
        self.invalid_item_id = 4000

    def tearDown(self):
        pass

    def test_verify_id_is_int_with_string(self):
        assert not Verify.verify_id_is_int("string")

    def test_verify_id_is_int_with_int(self):
        assert Verify.verify_id_is_int("9")

    def test_verify_bucketlist_exists_with_invalid_bucketlist(self):
        assert not Verify.verify_bucketlist_exists(bucketlist_id=self.invalid_bucketlist_id)

    def test_verify_bucketlist_exists_with_invalid_name(self):
        # 'r' is not a bucketlist name as of now
        assert not Verify.verify_bucketlist_exists(bucketlist_name="r")

    def test_verify_bucketlist_exists_with_valid_bucketlist_id(self):
        assert Verify.verify_bucketlist_exists(self.bucketlist.id)

    def test_verify_bucketlist_exists_with_valid_bucketlist_name(self):
        assert Verify.verify_bucketlist_exists(bucketlist_name=self.bucketlist.name)

    def test_verify_item_exists_with_invalid_item(self):
        assert not Verify.verify_item_exists(item_id=self.item.id)

    def test_verify_bucketlist_exists_with_invalid_item_name(self):
        # 'r' is not an item name as of now
        assert not Verify.verify_item_exists(item_name="r")

    def test_verify_item_exists_with_valid_item_id(self):
        assert Verify.verify_item_exists(item_id=self.item.id)

    def test_verify_item_exists_with_valid_item_name(self):
        assert Verify.verify_item_exists(item_name=self.item.name)

    def test_verify_password_with_invalid_password(self):
        assert not Verify.verify_user(self.bob.username, "unreal password")

    def test_verify_password_with_valid_credentials(self):
        assert Verify.verify_user(self.bob.username, "password")

    def test_verify_username_with_invalid_username(self):
        assert not Verify.verify_user("Not Bob", "password")

    def test_user_exists_with_invalid_email(self):
        assert not Verify.verify_user_exists(username=self.bob.username,
                                             email="bademail@mail.com")

    def test_user_exists_with_valid_email_and_username(self):
        assert Verify.verify_user_exists(username=self.bob.username,
                                         email=self.bob.email)

    def test_verify_email_with_invalid_email(self):
        assert not Verify.verify_valid_email("bademail@mail")

    def test_verify_email_with_valid_email(self):
        assert Verify.verify_valid_email("goodemail@mail.com")

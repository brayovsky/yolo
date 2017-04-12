from application.tests.base_test import BaseTestCase


class TestSingleBucketList(BaseTestCase):
    def setUp(self):
        super(TestSingleBucketList, self).setUp()
        # Log in user

    def tearDown(self):
        pass

    def test_does_not_retreive_with_invalid_id(self):
        pass

    def test_retreives_only_when_logged_in(self):
        pass

    def test_retreives_expected_json_with_valid_id(self):
        pass

    def test_does_not_update_with_invalid_id(self):
        pass

    def test_updates_only_when_logged_in(self):
        pass

    def test_updates_and_returns_expected_json(self):
        pass

    def test_does_not_delete_with_invalid_id(self):
        pass

    def test_deletes_only_when_logged_in(self):
        pass

    def test_deletes_and_returns_expected_json(self):
        pass

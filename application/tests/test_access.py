from application.tests.base_test import BaseTestCase


class TestSignUp(BaseTestCase):
    def setUp(self):
        super(TestSignUp, self).setUp()

    def tearDown(self):
        pass

    def test_does_not_signup_with_invalid_email(self):
        pass

    def test_does_not_signup_with_invalid_username(self):
        pass

    def test_does_not_signup_with_missing_parameters(self):
        pass

    def test_does_not_sign_up_existing_user(self):
        pass

    def test_signs_up_with_post_only(self):
        pass

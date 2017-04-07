from application.models.models import User, Bucketlists, Items

class Verify:
    """Holds methods for verifying input data from the user"""
    def verify_id_is_int(val):
        pass

    def verify_bucketlist_exists(bucketlist_id=None, bucketlist_name=None):
        """Verify bucketlist id or name exists in db"""
        pass

    def verify_item_exists(item_id=None, item_name=None):
        """Verify item_id exists in db"""
        pass

    def verify_valid_username(username):
        """Verify username is a valid username"""
        pass

    def verify_user_exists(username=None, email=None):
        """Verify username exists in db"""
        pass

    def verify_valid_email(email):
        """Verify email is a valid email"""
        pass

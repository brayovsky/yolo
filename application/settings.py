import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("YOLO_SECRET_KEY")
    # Track modifications might cause significant overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SITE_ROOT = os.environ.get("YOLO_SITE_ROOT", "http://127.0.0.1:5000")

    DATABASE_URL = None
    if os.environ.get("YOLO_DB") == "sqlite":
        DATABASE_URL = "sqlite:///" + os.path.join(basedir, "yolo.db")

    if os.environ.get("YOLO_DB") == "postgres":
        DATABASE_URL = os.environ.get("YOLO_DATABASE_URL")

    if os.environ.get("YOLO_DB") == "mysql":
        DATABASE_URL = os.environ.get("YOLO_DATABASE_URL")

    # Make an sqlite database by default
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or \
        "sqlite:///" + os.path.join(basedir, "yolo.db")


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # Get the test database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "YOLO_TEST_DATABASE_URL", "sqlite:///" + os.path.join(basedir,
                                                              "yolo_test.db"))

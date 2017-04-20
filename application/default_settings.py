import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("YOLO_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "yolo.db")
    # Track modifications might cause significant overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.environ.get("DB") == "postgres":
        DATABASE_URL = ""

    if os.environ.get("DB") == "mysql":
        DATABASE_URL = ""


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
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                              os.path.join(basedir, "yolo_test.db")

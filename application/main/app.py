from flask import Flask

app = Flask(__name__)

# Load configurations
app.config.from_object("application.default_settings.DevelopmentConfig")
app.config.from_envvar("YOLO_SETTINGS")

# Ignore pep8 to enable cyclic import
from application.models.models import User, db


@app.route('/')
def hello_world():
    new_user = User(username="huj", email="hbw@3", password="1")
    return 'Hello, World!'

print("app.py")

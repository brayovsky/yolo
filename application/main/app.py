import os

from flask import Flask

app = Flask(__name__)

# Load configurations
app.config.from_object("application.default_settings.DevelopmentConfig")
app.config.from_envvar("YOLO_SETTINGS")
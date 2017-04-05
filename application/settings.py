import os

from application.main.app import app

# Secret key for hashing passwords and tokens
app.config["SECRET_KEY"] = os.environ.get("YOLO_SECRET_KEY")

# Configure the database URI for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////yolo.db"

if os.environ.get("DB") == "postgres":
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

if os.environ.get("DB") == "mysql":
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

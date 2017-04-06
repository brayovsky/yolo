import os
from prompter import yesno

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application.main.app import app
from application.models.models import db


dirname, filename = os.path.split(os.path.abspath(__file__))
os.environ["SQLITE_DATABASE_PATH"] = 'sqlite:///' + \
                                        os.path.join(dirname, "yolo.db")

os.environ["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLITE_DATABASE_PATH")

app.config.from_object("application.models.models")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLITE_DATABASE_PATH")

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_database():
    "Creates database tables from sqlalchemy models"
    db.create_all()


@manager.command
def drop_database():
    "Drops database tables"
    if yesno("Are you sure you want to lose all your data"):
        db.drop_all()


if __name__ == '__main__':
    manager.run()

from prompter import yesno
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application.main.app import app
from application.models.models import db


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def create_database():
    """Creates database tables from sqlalchemy models"""
    # call configure_mappers() for search to work
    db.configure_mappers()
    db.create_all()


@manager.command
def drop_database():
    """Drops database tables"""
    if yesno("Are you sure you want to lose all your data"):
        db.drop_all()


if __name__ == "__main__":
    manager.run()

import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application.main.app import app
from application.models.models import User, db

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application/models/yolos.db'

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

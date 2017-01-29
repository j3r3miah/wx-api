import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database

from app import app, db
import app.models as app_models


manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on production.
    """
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']

    if database_exists(db_uri):
        drop_database(db_uri)
    create_database(db_uri)


if __name__ == '__main__':
    manager.run()

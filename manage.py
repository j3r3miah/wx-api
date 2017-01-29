import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database

from app import create_app
from app.models import User


app = create_app()
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on production.
    """
    db_uri = app.config['DATABASE_URI']

    if database_exists(db_uri):
        drop_database(db_uri)
    create_database(db_uri)

#     db.create_all()
#     db.session.commit()


if __name__ == '__main__':
    manager.run()

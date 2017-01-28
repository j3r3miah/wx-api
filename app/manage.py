import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import database_exists, create_database, drop_database

from flask_app import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)
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

    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()

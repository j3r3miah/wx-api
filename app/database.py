from flask import g

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def configure_db(app):
    engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True)

    session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    ))

    @app.before_request
    def attach_session():
        g.session = session()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)

    return session

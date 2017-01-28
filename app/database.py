from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def init_db(database_uri):
    engine = create_engine(database_uri, convert_unicode=True)

    global db_session
    db_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    ))

    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)

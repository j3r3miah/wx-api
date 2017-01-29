import pytest

from app import db, create_app


@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


@pytest.fixture(scope='session')
def database():
    db.create_all()


@pytest.fixture
def session(database):
    session = db.session
    yield session

    if session.dirty or session.new or session.deleted:
        if session.dirty:
            fail_msg = 'test completed with dirty session: {}'.format(
                session.dirty
            )
        if session.new:
            fail_msg = 'test completed with unflushed session: {}'.format(
                session.new
            )
        if session.deleted:
            fail_msg = 'test completed with unflushed session: {}'.format(
                session.deleted
            )
        session.rollback()
        session.close()
        pytest.fail(fail_msg)

    session.close()

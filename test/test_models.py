import pytest

from app.models import User


@pytest.fixture
def name():
    return 'jeremiah'


def test_user(session, name):
    user = User(name)
    assert user.name == name
    session.add(user)
    session.commit()
    assert session.query(User).filter(User.name == name).one()
    assert not session.query(User).filter(User.name == 'foo').all()

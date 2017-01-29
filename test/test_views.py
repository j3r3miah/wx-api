from app.models import User


def test_hello(client):
    res = client.get("/")
    assert res.status_code == 200
    assert 'hello' in str(res.data)


def test_post_user(session, client):
    name = 'dontcare'
    assert not session.query(User).filter(User.name == name).all()

    res = client.post("/users/", data=dict(name=name))
    assert res.status_code == 200
    assert '"name": "{}"'.format(name) in str(res.data)

    assert session.query(User).filter(User.name == name).one()

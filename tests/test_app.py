import json
from app import create_app, db


def setup_module(module):
    # use module-level app so tests can access it
    global app
    app = create_app()
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()


def teardown_module(module):
    with app.app_context():
        db.drop_all()


def test_register_login():
    client = app.test_client()
    # register
    r = client.post('/register', json={'username': 'test', 'password': 'pass'})
    assert r.status_code == 201
    # login
    r2 = client.post('/login', json={'username': 'test', 'password': 'pass'})
    assert r2.status_code == 200
    data = r2.get_json()
    assert 'access_token' in data


def test_courses_empty():
    client = app.test_client()
    r = client.get('/courses')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

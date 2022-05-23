from .utils import login, signup, logout, delete_user, admin_login


def test_login(client):
    admin_login(client)
    logout(client)


def test_signup(client):
    signup(client, 'test', 'test')


def test_delete_user(client):
    admin_login(client)
    delete_user(client, 'test')

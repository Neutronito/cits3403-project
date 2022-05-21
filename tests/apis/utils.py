from __future__ import annotations

import string
from contextlib import ContextDecorator, contextmanager
from flask_login import current_user, AnonymousUserMixin
import uuid
import secrets

from conftest import ADMIN_USER, ADMIN_PASSWORD


def login(client, username: str, password: str):
    r = client.post('/auth/login',
                    data={
                        'username': username,
                        'password': password,
                    })
    assert not isinstance(current_user, AnonymousUserMixin)
    assert current_user.name == username
    return r


def admin_login(client):
    return login(client, ADMIN_USER, ADMIN_PASSWORD)


def signup(client, username: str, password: str):
    r = client.post('/auth/signup',
                    data={'username': username,
                          'password': password,
                          'confirm': password,
                          'accept_tos': 'y',
                          'submit': 'Signup',
                          })
    assert not isinstance(current_user, AnonymousUserMixin)
    assert current_user.name == username
    return r


def logout(client):
    r = client.get('/auth/logout')
    assert isinstance(current_user, AnonymousUserMixin)
    return r


def delete_user(client, username: str):
    r = client.delete(f'/auth/api/user/{username}')
    assert r.status_code == 200, r.status_code
    return r


@contextmanager
def create_user(client, username: str | None = None, password: str | None = None) -> ContextDecorator:
    if username is None:
        username = uuid.uuid4().hex

    if password is None:
        password = ''.join(secrets.choice(string.ascii_letters) for _ in range(32))

    try:
        logout(client)
    except AssertionError:
        pass

    signup(client, username, password)
    yield username
    try:
        logout(client)
    except AssertionError:
        pass
    admin_login(client)
    delete_user(client, username)
    logout(client)


def create_map(client, html: str, date: str | None = None):
    r = client.post(f'/game/api/map?date={date}', data=html)
    assert r.status_code == 200
    return r

from flask import url_for
import uuid


def get_user(client):
    user_id = uuid.uuid4().hex
    res = client.delete(url_for('counter.user_endpoint', user_id=user_id))
    res = client.post(url_for('counter.user_endpoint', user_id=user_id))
    assert res.status_code == 200
    return user_id


def test_create_user(client):
    user_id = get_user(client)
    res = client.get(url_for('counter.count_endpoint', user_id=user_id))
    assert res.status_code == 200
    assert res.json['count'] == 0


def test_increment_count(client):
    user_id = get_user(client)
    res = client.put(url_for('counter.count_endpoint', user_id=user_id, action='increment'))
    assert res.status_code == 200
    assert res.json['count'] == 1


def test_increment_count_amount(client):
    user_id = get_user(client)
    res = client.put(url_for('counter.count_endpoint', user_id=user_id, action='increment', amount=3))
    assert res.status_code == 200
    assert res.json['count'] == 3


def test_decrement_count(client):
    user_id = get_user(client)
    res = client.put(url_for('counter.count_endpoint', user_id=user_id, action='decrement'))
    assert res.status_code == 200
    assert res.json['count'] == -1


def test_decrement_count_amount(client):
    user_id = get_user(client)
    res = client.put(url_for('counter.count_endpoint', user_id=user_id, action='decrement', amount=3))
    assert res.status_code == 200
    assert res.json['count'] == -3


def test_delete_user(client):
    user_id = get_user(client)
    res = client.delete(url_for('counter.user_endpoint', user_id=user_id))
    assert res.status_code == 200

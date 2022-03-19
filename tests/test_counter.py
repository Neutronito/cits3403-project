from flask import url_for


def test_index(client):
    assert client.get(url_for('counter.homepage')).status_code == 200

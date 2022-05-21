def test_page(client):
    r = client.get('/leaderboard/')
    assert r.status_code == 200


def test_get_latest(client):
    r = client.get('/leaderboard/api/latest')
    assert r.status_code == 200


def test_get_total(client):
    r = client.get('/leaderboard/api/total')
    assert r.status_code == 200


def test_get_all(client):
    r = client.get('/leaderboard/api/all')
    assert r.status_code == 200

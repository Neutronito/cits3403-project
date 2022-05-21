from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils import create_user, admin_login, create_map


def test_page(client):
    with create_user(client):
        r = client.get('/game/')
        assert r.status_code == 200


def test_map_endpoint(client):
    admin_login(client)
    html = "<h>Hello World</h>"
    date = "2022-08-01"
    r = client.post(f'/game/api/map?date={date}', data=html)
    assert r.status_code == 200

    r = client.get(f'/game/api/map?date={date}')
    assert r.status_code == 200
    assert html == r.get_json().get('html')

    r = client.delete(f'/game/api/map?date={date}')
    assert r.status_code == 200


def test_map_all_endpoint(client):
    admin_login(client)
    html = "<h>Hello World</h>"
    date = "2022-08-09"
    r = client.post(f'/game/api/map?date={date}', data=html)
    assert r.status_code == 200

    r = client.get('/game/api/map/all')
    assert r.status_code == 200
    assert len(r.get_json()) > 0

    r = client.delete(f'/game/api/map?date={date}')
    assert r.status_code == 200


def test_preview_endpoint(client):
    admin_login(client)
    r = client.post('/game/api/preview?width=100&height=30',
                    data="<h>Hello World</h>")
    assert r.status_code == 200
    assert r.get_json().get('data') is not None

    html = "<h>Hello darkness my old friend</h>"
    date = "2022-08-09"
    r = client.post(f'/game/api/map?date={date}', data=html)
    assert r.status_code == 200

    workers = 10
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(client.get, f'/game/api/preview?date={date}') for i in range(workers)]
        for future in as_completed(futures, timeout=30):
            r = future.result()
            assert r.status_code == 200
            assert r.get_json().get('data') is not None

    r = client.delete(f'/game/api/map?date={date}')
    assert r.status_code == 200


def test_score_endpoint(client):
    admin_login(client)

    html = "<h>Hello darkness my old friend</h>"
    date = "2022-08-09"
    create_map(client, html, date)

    r = client.post(f'/game/api/score?date={date}', data=html)
    assert r.status_code == 200
    assert r.get_json().get('submit_score') == 100

    r = client.post(f'/game/api/score?date={date}', data=html.replace('old', 'new'))
    assert r.status_code == 200
    assert r.get_json().get('submit_score') < 100

from .utils import admin_login, ADMIN_USER, create_user, logout


def test_panel(client):
    admin_login(client)
    r = client.get('/admin/')
    assert r.status_code == 200


def test_get_all_users(client):
    admin_login(client)
    r = client.get('/admin/api/user/all')
    assert r.status_code == 200
    assert len(r.get_json()['user_list']) >= 1


def test_is_admin(client):
    admin_login(client)
    r = client.get(f'/admin/api/user/is-admin?user={ADMIN_USER}')
    assert r.status_code == 200
    assert r.get_json().get('admin') is True


def test_make_admin(client):
    with create_user(client) as username:
        logout(client)
        admin_login(client)
        r = client.put(f'/admin/api/user/admin?adminFlag=true&user={username}')
        assert r.status_code == 204

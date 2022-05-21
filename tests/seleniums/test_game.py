from flask import url_for
from time import sleep
import pytest

from apis.utils import admin_login, create_map, create_user
from datetime import datetime


@pytest.mark.usefixtures('live_server')
def test_playing_game_get_score(selenium, client):
    admin_login(client)
    html = "<h> Hi welcome to coles online </h>"
    create_map(client, html, datetime.utcnow().date().isoformat())
    with create_user(client) as username:
        session = list(i for i in client.cookie_jar if i.name == 'session')[0]
        selenium.get(url_for('home.page', _external=True))
        selenium.add_cookie({"name": session.name, "value": session.value})
        selenium.get(url_for('game.page', _external=True))
        get_score_html = lambda: int(selenium.find_element_by_id("score").get_attribute('innerHTML').split()[-1])

        selenium.find_element_by_id("code").send_keys(html.replace("coles", "woolworths"))
        selenium.find_element_by_id("submit-button").click()
        sleep(1)
        assert 100 > get_score_html()

        selenium.find_element_by_id("code").clear()
        selenium.find_element_by_id("code").send_keys(html)
        selenium.find_element_by_id("submit-button").click()
        sleep(1)
        assert 100 == get_score_html()

import secrets
import string

import pytest
from flask_app import create_app
import os
import subprocess

ADMIN_USER = 'admin'
ADMIN_PASSWORD = ''.join(secrets.choice(string.ascii_letters) for _ in range(32))
basedir = os.path.dirname(__file__)


@pytest.fixture(scope='session')
def app():
    os.environ['WTF_CSRF_ENABLED'] = 'false'
    os.environ['TESTING'] = 'true'
    sqlite_db_path = f'{basedir}/sqlite.db'
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + sqlite_db_path

    try:
        os.remove(sqlite_db_path)
    except FileNotFoundError:
        pass

    subprocess.run(['flask-db', 'upgrade'],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(['flask-create-admin', '-u', ADMIN_USER, '-p', ADMIN_PASSWORD],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    app = create_app()
    return app


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    return chrome_options

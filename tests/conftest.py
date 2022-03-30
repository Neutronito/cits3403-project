import pytest
from flask_app import create_app
from flask_app.models.count import SqliteCountModel
import tempfile


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def count_model():
    with tempfile.NamedTemporaryFile() as fp:
        m = SqliteCountModel(fp.name)
        yield m
        m.close()

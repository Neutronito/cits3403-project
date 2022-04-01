from flask import Flask
from .controllers.counter import counter
from .models.count import SqliteCountModel
from dotenv import load_dotenv
import os

basedir = os.path.dirname(__file__)


def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.register_blueprint(counter)
    app.config['dpath'] = os.path.join(basedir, 'sqlite.db')
    return app


def main() -> int:
    load_dotenv(os.path.join(basedir, '.flaskenv'))
    create_app().run(debug=True)
    return 0

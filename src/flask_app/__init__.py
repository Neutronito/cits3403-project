import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .controllers.counter import counter

basedir = os.path.dirname(__file__)
db = SQLAlchemy()

from .models import countv2


def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.register_blueprint(counter)
    app.config['dpath'] = os.path.join(basedir, 'sqlite.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    db.create_all(app=app)

    return app


def main() -> int:
    load_dotenv(os.path.join(basedir, '.flaskenv'))
    create_app().run(debug=True)
    return 0


def shell():
    import subprocess
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    load_dotenv(os.path.join(basedir, '.flaskenv'))
    my_env = os.environ.copy()
    my_env['FLASK_APP'] = basedir
    subprocess.run(['flask', 'shell'], env=my_env)

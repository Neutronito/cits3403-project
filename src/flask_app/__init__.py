from flask import Flask
from .controllers.counter import counter
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.register_blueprint(counter)
    return app


def main() -> int:
    load_dotenv(os.path.join(os.path.dirname(__file__), '.flaskenv'))
    create_app().run(debug=True)
    return 0

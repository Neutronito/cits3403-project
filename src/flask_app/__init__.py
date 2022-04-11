import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_login import LoginManager
from flask_app.controllers.counter import counter


basedir = os.path.dirname(__file__)
db = SQLAlchemy()
login_manager = LoginManager()

from flask_app.models import count


@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(count.User, user_id)


def model_exists(model_class):
    engine = db.get_engine(bind=model_class.__bind_key__)
    return model_class.metadata.tables[model_class.__tablename__].exists(engine)


def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static')
    app.register_blueprint(counter)
    app.config.from_pyfile('settings.py')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        inspector = inspect(db.engine)
        first_time_create_admin = not inspector.has_table(count.User.__tablename__)
    db.create_all(app=app)
    if first_time_create_admin:
        with app.app_context():
            create_admin_func(app.config['DEFAULT_ADMIN_USERNAME'], app.config['DEFAULT_ADMIN_PASSWORD'])

    return app


def shell():
    import subprocess
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    load_dotenv(os.path.join(basedir, '.flaskenv'))
    my_env = os.environ.copy()
    my_env['FLASK_APP'] = basedir
    subprocess.run(['flask', 'shell'], env=my_env)


def create_admin_func(username, password):
    user = count.User(name=username, password=password, admin=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    count_r = count.Count(username=username)
    db.session.add(count_r)
    db.session.commit()


def create_admin() -> int:
    from getpass import getpass
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    app = create_app()
    with app.app_context():
        create_admin_func(username, password)
    print("admin account has been created")
    return 0


def main() -> int:
    load_dotenv(os.path.join(basedir, '.flaskenv'))
    create_app().run(debug=True)
    return 0


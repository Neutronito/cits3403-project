# https://prettyprinted.com/tutorials/automatically_load_environment_variables_in_flask

import os

SECRET_KEY = os.getenv('SECRET_KEY', 'banana')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///sqlite.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')

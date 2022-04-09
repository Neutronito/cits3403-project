from typing import ContextManager
from contextlib import contextmanager

from flask import Blueprint, render_template, current_app, request, jsonify
from flask_app.models.count import SqliteCountModel, AbstractCountModel
counter = Blueprint('counter', __name__)


@contextmanager
def get_count_model() -> ContextManager[AbstractCountModel]:
    count_model = SqliteCountModel(dpath=current_app.config['dpath'])
    try:
        yield count_model
    finally:
        count_model.close()


@counter.route('/')
def homepage():  # put application's code here
    return render_template('homepage.html')


@counter.route('/login')
def login(): 
    return render_template('login.html')


@counter.route('/api/v1/user/<user_id>', methods=['POST', 'DELETE'])
def user_endpoint(user_id: str):
    with get_count_model() as count_model:
        if request.method == 'POST':
            count_model.add_user(user_id=user_id)
            return jsonify({
                "count": 0
            })
        elif request.method == 'DELETE':
            count_model.remove_user(user_id=user_id)
            return "user has been deleted", 200


@counter.route('/api/v1/count/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def count_endpoint(user_id: str):
    with get_count_model() as count_model:
        if request.method == 'GET':
            return jsonify({
                "count": count_model.get_count(user_id=user_id)
            })

        elif request.method == 'PUT':
            action = request.args.get('action')
            amount = int(request.args.get('amount', 1))
            if action == 'increment':
                for _ in range(amount):
                    count_model.increment_count(user_id=user_id)
            elif action == 'decrement':
                for _ in range(amount):
                    count_model.decrement_count(user_id=user_id)
            else:
                return jsonify({
                    "error": "please choose either 'increment' or 'decrement' in the 'action' parameter"
                }), 400

            return jsonify({
                "count": count_model.get_count(user_id=user_id)
            })

        elif request.method == 'DELETE':
            count_model.reset_count(user_id=user_id)
            return jsonify({
                "count": 0
            })

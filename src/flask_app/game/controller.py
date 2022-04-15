from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required

from flask_app.auth.controller import admin_required

game = Blueprint('game', __name__, template_folder='views', static_folder='static')


@game.route("/", methods=["GET"])
@login_required
def page():
    return render_template('game.html')


@game.route('/api/user/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def user_endpoint(user_id: str):
    from flask_app.auth.models import User
    from flask_app import db
    user = User.query.get(user_id)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return "user has been deleted", 200


@game.route('/api/count', methods=['GET', 'POST', 'DELETE'])
@login_required
def count_endpoint():
    from flask_app import db
    from flask_app.auth.models import User
    args = request.args

    if current_user.admin and 'user' in args:
        count_row = User.query.get(args['user'])
    else:
        count_row = current_user.count

    if request.method == 'GET':
        return jsonify({
            "count": count_row.count
        })

    elif request.method == 'POST':
        action = args.get('action')
        amount = int(args.get('amount', 1))
        if action == 'increment':
            count_row.count += amount
        elif action == 'decrement':
            count_row.count -= amount
        else:
            return jsonify({
                "error": "please choose either 'increment' or 'decrement' in the 'action' parameter"
            }), 400

        db.session.add(count_row)
        db.session.commit()

        return jsonify({
            "count": count_row.count
        })

    elif request.method == 'DELETE':
        count_row.count = 0
        db.session.add(count_row)
        db.session.commit()
        return jsonify({
            "count": 0
        })

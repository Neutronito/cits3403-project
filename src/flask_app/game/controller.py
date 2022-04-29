from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime

from flask_app.auth.controller import admin_required

game = Blueprint('game', __name__, template_folder='views', static_folder='static')


@game.route("/", methods=["GET"])
@login_required
def page():
    return render_template('game.html')


@game.route('/api/count', methods=['GET', 'POST', 'DELETE'])
@login_required
def count_endpoint():
    from flask_app import db
    from flask_app.auth.models import User
    from flask_app.game.models import Count
    args = request.args

    if current_user.admin and 'date' in args:
        try:
            date = datetime.fromisoformat(args['date']).date()
        except ValueError:
            return "invalid date", 422
    else:
        date = None

    if current_user.admin and 'user' in args:
        user = User.query.get(args['user'])
    else:
        user = current_user

    if date is None:
        count_row = user.get_today_count()
    else:
        count_row = db.session.query(Count).filter_by(username=user.name, date=date).first()
        if count_row is None:
            count_row = Count(username=user.name, date=date)

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

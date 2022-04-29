from flask import Blueprint, render_template, jsonify

leaderboard = Blueprint('leaderboard', __name__, template_folder='views', static_folder='static')


@leaderboard.route('/')
def page():  # put application's code here
    return render_template('leaderboard.html')


@leaderboard.route("/api/latest", methods=["GET"])
def get_latest():
    from flask_app.auth.models import User

    data_list = []

    query = User.query.all()    
    for user in query:
        data_list.append({"name": user.name, "count": user.get_today_count().count})
    
    return jsonify(data_list), 200


@leaderboard.route("/api/total", methods=["GET"])
def get_total():
    from flask_app.auth.models import User

    data_list = []

    query = User.query.all()
    for user in query:
        data_list.append({"name": user.name, "count": sum(i.count for i in user.count)})

    return jsonify(data_list), 200


@leaderboard.route("/api/all", methods=["GET"])
def get_all():
    from flask_app.auth.models import User

    data_list = []

    query = User.query.all()
    for user in query:
        for count in user.count:
            data_list.append({"date": count.date.isoformat(), "name": user.name, "count": count.count})
    return jsonify(data_list), 200

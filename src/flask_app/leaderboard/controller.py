from flask import Blueprint, render_template, jsonify

leaderboard = Blueprint('leaderboard', __name__, template_folder='views', static_folder='static')


@leaderboard.route('/')
def page():  # put application's code here
    return render_template('leaderboard.html')

@leaderboard.route("/api/user/all", methods=["GET"])
def get_all():
    from flask_app import db
    from flask_app.auth.models import User

    data_list = []

    query = User.query.all()    
    for user in query:
        temp_dict = {"name":user.name, "count":user.count.count}
        data_list.append(temp_dict)
    
    return jsonify(data_list), 200

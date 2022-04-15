from flask import Blueprint, render_template

leaderboard = Blueprint('leaderboard', __name__, template_folder='views', static_folder='static')


@leaderboard.route('/')
def page():  # put application's code here
    return render_template('leaderboard.html')

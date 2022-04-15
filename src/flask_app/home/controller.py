from flask import Blueprint, render_template

home = Blueprint('home', __name__, template_folder='views', static_folder='static')


@home.route('/')
def page():  # put application's code here
    return render_template('homepage.html')

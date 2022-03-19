from flask import Blueprint, render_template

counter = Blueprint('counter', __name__)


@counter.route('/')
def homepage():  # put application's code here
    return render_template('counter.html')

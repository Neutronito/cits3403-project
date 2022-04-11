import functools
from http import HTTPStatus

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, abort
from flask_login import current_user, login_user, login_required, logout_user

from flask_app.forms import LoginForm, SignupForm

counter = Blueprint('counter', __name__)


@counter.route('/')
def homepage():  # put application's code here
    return render_template('homepage.html')


@counter.route('/login',  methods=['GET', 'POST'])
def login():
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    from flask_app.models.count import User
    if current_user.is_authenticated:
        return redirect(url_for('counter.homepage'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('counter.login'))

        login_user(user, remember=form.remember_me.data)
        flash('successful login')
        if user.admin:
            return redirect(url_for('counter.admin'))
        else:
            return redirect(url_for('counter.game'))

    return render_template('login.html', form=form)


@counter.route('/signup',  methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('counter.homepage'))

    form = SignupForm()

    if form.validate_on_submit():
        from flask_app.models.count import User, Count
        from flask_app import db
        user = User(name=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        count = Count(username=user.name)
        db.session.add(count)
        db.session.commit()
        flash("Thank you")
        return redirect(url_for('counter.login'))

    return render_template('signup.html', form=form)


@counter.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for('counter.homepage'))


@counter.route("/tos", methods=["GET"])
def tos():
    return render_template('tos.html')


@counter.route("/game", methods=["GET"])
@login_required
def game():
    return render_template('game.html')


def check_admin():
    if not current_user.admin:
        abort(HTTPStatus.UNAUTHORIZED)


def admin_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        check_admin()
        return func(*args, **kwargs)
    return decorated_view


@counter.route("/admin", methods=["GET"])
@login_required
@admin_required
def admin():
    return render_template('admin.html')


@counter.route('/api/v1/user/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def user_endpoint(user_id: str):
    from flask_app.models.count import User
    from flask_app import db
    user = User.query.get(user_id)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return "user has been deleted", 200


@counter.route('/api/v1/count', methods=['GET', 'POST', 'DELETE'])
@login_required
def count_endpoint():
    from flask_app import db
    from flask_app.models.count import User
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
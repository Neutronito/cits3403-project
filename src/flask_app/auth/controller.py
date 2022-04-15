import functools
from http import HTTPStatus

from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_user, login_required, logout_user

from flask_app.auth.forms import LoginForm, SignupForm

auth = Blueprint('auth', __name__, template_folder='views', static_folder='static')


@auth.route('/login',  methods=['GET', 'POST'])
def login():
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
    from flask_app.auth.models import User
    if current_user.is_authenticated:
        return redirect(url_for('home.page'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        flash('successful login')
        if user.admin:
            return redirect(url_for('admin.panel'))
        else:
            return redirect(url_for('game.page'))

    return render_template('login.html', form=form)


@auth.route('/signup',  methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('home.page'))

    form = SignupForm()

    if form.validate_on_submit():
        from flask_app.auth.models import User
        from flask_app.game.models import Count
        from flask_app import db
        user = User(name=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        count = Count(username=user.name)
        db.session.add(count)
        db.session.commit()
        flash("Thank you")

        # Log the user in
        login_user(user)
        return redirect(url_for('game.page'))

    return render_template('signup.html', form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for('home.page'))


@auth.route("/tos", methods=["GET"])
def tos():
    return render_template('tos.html')


def check_admin():
    if not current_user.admin:
        abort(HTTPStatus.UNAUTHORIZED)


def admin_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        check_admin()
        return func(*args, **kwargs)
    return decorated_view

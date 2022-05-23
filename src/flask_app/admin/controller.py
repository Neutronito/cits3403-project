from contextlib import redirect_stderr
from crypt import methods
from operator import methodcaller
from flask import render_template, Blueprint, jsonify, request, redirect, url_for
from flask_app.admin.forms import newMapForm
from flask_login import login_required, current_user
from flask import app

from flask_app.auth.controller import admin_required

admin = Blueprint('admin', __name__, template_folder='views', static_folder='static')


@admin.route("/", methods=["GET", "POST"])
@login_required
@admin_required
def panel():
    form = newMapForm()
    if form.validate_on_submit():

        from flask_app import db
        from flask_app.game.models import Map
        the_map = Map(date=form.date.data,
                    username=current_user.name,
                    html=form.map.data,
                    width=form.width.data,
                    height=form.height.data)
        
        db.session.add(the_map)
        db.session.commit()

        return redirect(url_for('admin.panel'))
    if request.method == 'GET':
        return render_template('admin.html', form=form, map_active="active", map_show_active="show active")
    elif request.method == 'POST':
        return render_template('admin.html', form=form, add_active="active", add_show_active="show active")

@admin.route("/api/user/all", methods=["GET"])
@login_required
@admin_required
def get_all():
    from flask_app import db
    from flask_app.auth.models import User

    user_list = []
    query = User.query.all()    
    for user in query:
        user_list.append(user.name)
    
    return jsonify({
            "user_list": user_list
        })

@admin.route("/api/user/is-admin", methods=["GET"])
@login_required
@admin_required
def get_is_admin():
    from flask_app import db
    from flask_app.auth.models import User

    args = request.args
    if 'user' in args:
        isAdmin = User.query.get(args['user']).admin
        return jsonify({
            "admin": isAdmin
        })
    else:
        return jsonify({
                "error": "Please give a user in the 'user' parameter"
            }), 400

@admin.route("/api/user/admin", methods=["PUT"])
@login_required
@admin_required
def change_admin():
    from flask_app import db
    from flask_app.auth.models import User

    args = request.args
    if 'user' in args:
        adminFlag = args.get('adminFlag')
        if adminFlag == 'true':
            user = User.query.get(args['user'])
            user.admin = True
        elif adminFlag == 'false':
            user = User.query.get(args['user'])
            user.admin = False
        else:
            return jsonify({
                "error": "Please choose either 'true' or 'false' in the 'adminFlag' parameter"
            }), 400
        db.session.add(user)
        db.session.commit()
        return '', 204 
    else: 
        return jsonify({
                "error": "Please give a user in the 'user' parameter"
            }), 400

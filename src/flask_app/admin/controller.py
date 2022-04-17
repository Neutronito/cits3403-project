from crypt import methods
from operator import methodcaller
from flask import render_template, Blueprint, jsonify, request
from flask_login import login_required  
from flask import app

from flask_app.auth.controller import admin_required

admin = Blueprint('admin', __name__, template_folder='views', static_folder='static')


@admin.route("/", methods=["GET"])
@login_required
@admin_required
def panel():
    return render_template('admin.html')

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

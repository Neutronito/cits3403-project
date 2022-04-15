from flask import render_template, Blueprint
from flask_login import login_required

from flask_app.auth.controller import admin_required

admin = Blueprint('admin', __name__, template_folder='views', static_folder='static')


@admin.route("/", methods=["GET"])
@login_required
@admin_required
def panel():
    return render_template('admin.html')

from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from tempfile import TemporaryDirectory
import os
from html2image import Html2Image
import io
from PIL import Image

from flask_app.auth.controller import admin_required

game = Blueprint('game', __name__, template_folder='views', static_folder='static')


@game.route("/", methods=["GET"])
@login_required
def page():
    return render_template('game.html')


@game.route('/api/count', methods=['GET', 'POST', 'DELETE'])
@login_required
def count_endpoint():
    from flask_app import db
    from flask_app.auth.models import User
    from flask_app.game.models import Count
    args = request.args

    if current_user.admin and 'date' in args:
        try:
            date = datetime.fromisoformat(args['date']).date()
        except ValueError:
            return "invalid date", 422
    else:
        date = None

    if current_user.admin and 'user' in args:
        user = User.query.get(args['user'])
    else:
        user = current_user

    if date is None:
        count_row = user.get_today_count()
    else:
        count_row = db.session.query(Count).filter_by(username=user.name, date=date).first()
        if count_row is None:
            count_row = Count(username=user.name, date=date)

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


@game.route('/api/map', methods=['GET', 'POST', 'DELETE'])
@login_required
def map_endpoint():
    from flask_app import db
    from flask_app.game.models import Map
    args = request.args

    if current_user.admin and 'date' in args:
        try:
            date = datetime.fromisoformat(args['date']).date()
        except ValueError:
            return "invalid date", 422
    else:
        date = None

    if request.method == 'GET':
        the_map = Map.get_map(date)
        if the_map is None:
            return jsonify(None), 204
        else:
            the_map_dict = the_map.to_dict()
            if not current_user.admin:
                the_map_dict.pop('html')
            return jsonify(the_map_dict), 200

    elif request.method == 'POST':
        if (width := args.get('width', 300)) is not None:
            width = int(width)

        if (height := args.get('height', 300)) is not None:
            height = int(height)

        the_map = Map(date=date,
                      username=current_user.name,
                      html=request.get_data(as_text=True),
                      width=width,
                      height=height)
        db.session.add(the_map)
        db.session.commit()
        return "success", 200

    elif request.method == 'DELETE':
        if date is None:
            return "date parameter must be provided", 422
        the_map = Map.get_map(date)
        db.session.delete(the_map)
        db.session.commit()
        return "success", 200


@game.route('/api/map/all', methods=['GET'])
@login_required
@admin_required
def map_all_endpoint():
    from flask_app.game.models import Map
    map_list = []
    query = Map.query.all()
    a_map: Map
    for a_map in query:
        map_list.append(a_map.to_dict())
    return jsonify(map_list), 200


def get_image_binary(html: str, width: int, height: int) -> bytes:
    with TemporaryDirectory() as dp:
        hti = Html2Image(custom_flags=["--no-sandbox", "--hide-scrollbars"], output_path=dp)
        hti.screenshot(html_str=html, save_as="screenshot.png", size=(width, height))
        with open(os.path.join(dp, "screenshot.png"), 'rb') as fp:
            return fp.read()


def byes_to_image(data: bytes) -> Image:
    return Image.open(io.BytesIO(data))


@game.route('/api/preview', methods=['GET', 'POST'])
@login_required
def preview_endpoint():
    import base64
    from flask_app.game.models import Map
    args = request.args
    if (width := args.get('width', 300)) is not None:
        width = int(width)

    if (height := args.get('height', 300)) is not None:
        height = int(height)

    if request.method == 'GET':
        if current_user.admin and 'date' in args:
            try:
                date = datetime.fromisoformat(args['date']).date()
            except ValueError:
                return "invalid date", 422
        else:
            date = None
        the_map = Map.get_map(date)
        html = the_map.html
    else:
        html = request.get_data(as_text=True)

    image = get_image_binary(html=html, width=width, height=height)
    return jsonify({"data": base64.b64encode(image).decode()}), 200


def normalize(value: float, skewness: float = 2) -> int:
    # because the scores sometimes can get very high, to normalize this a bit we lower
    # the higher end values, here is the graph https://www.desmos.com/calculator/eqxcp2tgz2
    norm = -(-value + 1)**(1/skewness) + 1
    return int(norm * 100)


@game.route('/api/score', methods=['POST'])
@login_required
def score_endpoint():
    from flask_app.game.models import Map
    from SSIM_PIL import compare_ssim
    body = request.get_data(as_text=True)
    args = request.args
    if current_user.admin and 'date' in args:
        try:
            date = datetime.fromisoformat(args['date']).date()
        except ValueError:
            return "invalid date", 422
    else:
        date = None

    the_map = Map.get_map(date)

    the_map_image = byes_to_image(get_image_binary(html=the_map.html, width=the_map.width, height=the_map.height))
    the_other_image = byes_to_image(get_image_binary(html=body, width=the_map.width, height=the_map.height))
    score = normalize(compare_ssim(the_map_image, the_other_image, GPU=False))
    return jsonify({"score": score}), 200

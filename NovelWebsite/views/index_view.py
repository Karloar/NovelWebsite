from flask import Blueprint
from flask import render_template
from ..models import db
from ..models import NovelType


index_view = Blueprint(__name__, 'index_view')


@index_view.route("/", methods=["GET"])
def index():
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    return render_template("index.html", data=data)


@index_view.route("/category/<int:type_id>", methods=['GET'])
def category(type_id):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['type_id'] = type_id
    return render_template("index.html", data=data)

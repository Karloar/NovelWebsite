from flask import Blueprint
from flask import render_template
from ..models import db
from ..models import NovelType
from ..models import NovelTitle
from ..models import NovelSection


index_view = Blueprint(__name__, 'index_view')


@index_view.route("/", methods=["GET"])
def index():
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['suggestion_list'] = db.session.query(
        NovelTitle.id,
        NovelTitle.name,
        NovelTitle.author,
        NovelTitle.cover,
        NovelTitle.introduction,
        NovelType.name.label("type_name"),
    ).outerjoin(NovelType).group_by(NovelTitle.id).order_by(
        NovelTitle.read_num.desc(),
        NovelTitle.id.asc(),
    ).limit(19)
    data['category_novel_list'] = dict()
    for novel_type in data['type_list']:
        data['category_novel_list'][novel_type.id] = db.session.query(NovelTitle).filter(
            NovelTitle.type_id == novel_type.id
        ).order_by(
            NovelTitle.read_num.desc(),
            NovelTitle.id.asc(),
        ).limit(6)
    data['last_update_novel_list'] = db.session.query(
        NovelTitle.id.label('title_id'),
        NovelTitle.name.label('title_name'),
        NovelTitle.author,
        NovelSection.title.label('section_name'),
        NovelSection.id.label('section_id'),
        NovelType.name.label('type_name')
    ).join(NovelSection, NovelType).order_by(NovelSection.id.desc()).limit(20)
    data['last_append_novel_list'] = db.session.query(
        NovelTitle.id.label('title_id'),
        NovelTitle.name.label('title_name'),
        NovelTitle.author,
        NovelType.name.label('type_name')
    ).join(NovelType).order_by(NovelTitle.id).limit(20)
    db.session.remove()
    return render_template("index.html", data=data)


@index_view.route("/category/<int:type_id>", methods=['GET'])
def category(type_id):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['type_id'] = type_id
    data['type_name'] = db.session.query(NovelType).filter(NovelType.id == type_id).one().name
    db.session.remove()
    return render_template("category.html", data=data)


@index_view.route("/hehe/<int:novel_id>")
@index_view.route("/novel/<int:novel_id>", methods=['GET'])
def novel(novel_id):
    return str(novel_id)

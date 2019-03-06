from flask import Blueprint
from flask import render_template
from ..models import db
from ..models import NovelType
from ..models import NovelTitle
from ..models import NovelSection
from . import error_processing


index_view = Blueprint(__name__, 'index_view')


@index_view.route("/", methods=["GET"])
@error_processing
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
    ).join(NovelType).order_by(NovelTitle.id.desc()).limit(20)
    data['index'] = True
    db.session.remove()
    return render_template("index.html", data=data)


@index_view.route("/category/<int:type_id>", methods=['GET'])
@index_view.route("/category/<int:type_id>/<int:page>", methods=['GET'])
@error_processing
def category(type_id, page=1):
    data = dict()
    per_page = 25
    data['current_page'] = page
    data['total'] = db.session.query(NovelSection.id).join(NovelTitle).filter(NovelTitle.type_id == type_id).count()
    data['page_num'] = data['total'] // per_page if data['total'] % per_page == 0 else data['total'] // per_page + 1
    if page > data['page_num']:
        raise Exception('over max pages')
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['type_id'] = type_id
    data['type_name'] = db.session.query(NovelType).filter(NovelType.id == type_id).one().name
    data['top_novels'] = db.session.query(
        NovelTitle.id,
        NovelTitle.name,
        NovelTitle.author,
        NovelTitle.cover,
        NovelTitle.introduction
    ).filter(NovelTitle.type_id == type_id).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(6)
    data['last_update_novel_list'] = db.session.query(
        NovelTitle.id.label('title_id'),
        NovelTitle.name.label('title_name'),
        NovelTitle.author,
        NovelType.name.label('type_name'),
        NovelSection.title.label("section_name")
    ).join(NovelType, NovelSection).filter(NovelTitle.type_id == type_id).order_by(
        NovelSection.id.desc()
    ).offset(per_page * (page - 1)).limit(per_page)
    data['recommend_novel_list'] = db.session.query(
        NovelTitle.id.label('title_id'),
        NovelTitle.name.label('title_name'),
        NovelTitle.author,
        NovelType.name.label('type_name')
    ).join(NovelType).filter(NovelTitle.type_id == type_id).order_by(
        NovelTitle.read_num.desc(),
        NovelTitle.id.asc()
    ).limit(per_page + 2)
    db.session.remove()
    return render_template("category.html", data=data)


@index_view.route("/novel/<int:novel_id>", methods=['GET'])
@error_processing
def novel(novel_id):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['novel'] = db.session.query(
        NovelTitle.id.label('title_id'),
        NovelTitle.name.label('title_name'),
        NovelTitle.author,
        NovelTitle.type_id,
        NovelTitle.introduction,
        NovelTitle.cover,
        NovelType.name.label('type_name')
    ).join(NovelType).filter(NovelTitle.id == novel_id).one()
    data['novel_sections'] = db.session.query(
        NovelSection
    ).filter(NovelSection.novel_id == novel_id).order_by(NovelSection.novel_id.asc())
    data['recommend_novel_list'] = db.session.query(NovelTitle).filter(
        NovelTitle.type_id == data['novel'].type_id
    ).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(5)
    data['novel_sections_new'] = db.session.query(
        NovelSection
    ).filter(NovelSection.novel_id == novel_id).order_by(NovelSection.id.desc()).limit(6)
    db.session.remove()
    return render_template("novel.html", data=data)


@index_view.route("/detail/<int:section_id>", methods=['GET'])
@error_processing
def detail(section_id):
    return str(section_id)

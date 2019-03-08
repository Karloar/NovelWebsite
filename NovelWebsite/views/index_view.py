from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect
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
        NovelSection.title.label("section_name"),
        NovelSection.id.label('section_id')
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
        NovelTitle.type_id == data['novel'].type_id,
        NovelTitle.id != novel_id
    ).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(5)
    data['novel_sections_new'] = db.session.query(
        NovelSection
    ).filter(NovelSection.novel_id == novel_id).order_by(NovelSection.id.desc()).limit(12)
    db.session.remove()
    return render_template("novel.html", data=data)


@index_view.route("/detail/<int:section_id>", methods=['GET'])
@error_processing
def detail(section_id):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['section'] = db.session.query(NovelSection).filter(NovelSection.id == section_id).one()
    data['content'] = [
        x.strip() for x in data['section'].content.split('<br />') if x.strip() and (
                "http://www.shuquge.com/" not in x and "请记住本书首发域名" not in x
        )
    ]
    data['recommend_novel_list'] = db.session.query(NovelTitle).filter(
        NovelTitle.id != data['section'].novel_title.id
    ).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(5)
    section_id_list = [x.id for x in db.session.query(NovelSection.id).filter(
        NovelSection.novel_id == data['section'].novel_title.id
    ).order_by(NovelSection.id.asc())]
    current = section_id_list.index(data['section'].id)
    data['previous'] = section_id_list[current-1] if current else section_id_list[0]
    data['next'] = section_id_list[current+1] if current < len(section_id_list)-1 else section_id_list[-1]
    db.session.remove()
    if 'content_style' in session:
        data['content_style'] = session['content_style']
        temp_list = []
        for k, v in session['content_style'].items():
            temp_list.append('{0}: {1};'.format(k, v))
        data['content_style_str'] = ''.join(temp_list)
    data['font-family'] = [
        ("", "字体"), ("", "默认"),
        ("黑体", "黑体"), ("楷体_GB2312", "楷体"),
        ("微软雅黑", "微软雅黑"), ("方正启体简体", "启体"),
        ("宋体", "宋体")
    ]
    data['color'] = [
        ("", "颜色"), ("", "默认"),
        ("rgb(147, 112, 219)", "暗紫"), ("rgb(46, 139, 87)", "藻绿"),
        ("rgb(47, 79, 79)", "深灰"), ("rgb(119, 136, 153)", "青灰"),
        ("rgb(128, 0, 0)", "栗色"), ("rgb(106, 90, 205)", "青蓝"),
        ("rgb(188, 143, 143)", "玫褐"), ("rgb(244, 164, 96)", "黄褐"),
    ]
    data['font-size'] = [
        ("15pt", "大小"), ("15pt", "默认"),
        ("11pt", "11pt"), ("13pt", "13pt"),
        ("17pt", "17pt"), ("20pt", "20pt"),
        ("23pt", "23pt"), ("25pt", "25pt"),
        ("27pt", "27pt"), ("30pt", "30pt"),
    ]

    novel_title = data['section'].novel_title
    if 'novel_' + str(novel_title.id) not in session:
        novel_title = data['section'].novel_title
        novel_title.read_num += 1
        db.session.query(NovelTitle).filter(
            NovelTitle.id == novel_title.id
        ).update({NovelTitle.read_num: novel_title.read_num})
        db.session.commit()
        session['novel_' + str(novel_title.id)] = 'true'

    return render_template("detail.html", data=data)


@index_view.route("/save_novel_content_style", methods=['GET'])
@error_processing
def save_novel_content_style():
    session['content_style'] = {
        'font-size': request.args.get('font-size', ''),
        'font-family': request.args.get('font-family', ''),
        'color': request.args.get('color', ''),
    }
    return "success"


@index_view.errorhandler(404)
def error_404(error):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    db.session.remove()
    return render_template("error_404.html", data=data)


@index_view.route("/search", methods=['POST'])
@error_processing
def first_search():
    session['search_word'] = request.form['search_word']
    return redirect("/search/1")


@index_view.route("/search/category/<int:category_id>/<int:page>", methods=['GET'])
@index_view.route("/search/<int:page>", methods=['GET'])
@error_processing
def search(category_id=None, page=1):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    per_page = 20
    data['base_url'] = request.base_url.rsplit("/", maxsplit=1)[0]
    data['current_page'] = page
    if category_id:
        data['search_results'] = db.session.query(NovelTitle).join(NovelType).filter(
            NovelType.id == category_id,
            db.or_(
                NovelTitle.name.like('%{0}%'.format(session['search_word'])),
                NovelTitle.author.like('%{0}%'.format(session['search_word'])))
        ).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).offset((page - 1) * per_page).limit(per_page)
        novel_num = db.session.query(NovelTitle).join(NovelType).filter(
            NovelType.id == category_id,
            db.or_(
                NovelTitle.name.like('%{0}%'.format(session['search_word'])),
                NovelTitle.author.like('%{0}%'.format(session['search_word'])))
        ).count()
    else:
        data['search_results'] = db.session.query(NovelTitle).filter(
            db.or_(
                NovelTitle.name.like('%{0}%'.format(session['search_word'])),
                NovelTitle.author.like('%{0}%'.format(session['search_word'])))
        ).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).offset((page - 1) * per_page).limit(per_page)
        novel_num = db.session.query(NovelTitle).filter(
            db.or_(
                NovelTitle.name.like('%{0}%'.format(session['search_word'])),
                NovelTitle.author.like('%{0}%'.format(session['search_word'])))
        ).count()
    data['total_page'] = novel_num // per_page if novel_num % per_page == 0 else novel_num // per_page + 1
    db.session.remove()
    return render_template('search.html', data=data)

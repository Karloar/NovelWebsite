from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect
from flask import jsonify
from . import error_processing
from . import get_base_url_for_pagination
from ..models import db
from ..models import NovelTitle
from ..models import NovelSection
from ..models import NovelType
from ..models import User
from ..models import UserCollection


admin_view = Blueprint('admin_view', __name__)


@admin_view.route("/admin/users/<int:page>", methods=["GET"])
@admin_view.route("/admin/users", methods=['GET'])
@error_processing
def admin_users(page=1):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    per_page = 20
    data['current_page'] = page
    data['base_url'] = get_base_url_for_pagination(request.base_url, page)
    data['users'] = db.session.query(User).filter(
        db.func.lower(User.name) != 'admin'
    ).order_by(User.id.asc()).offset((page - 1) * per_page).limit(per_page)
    user_num = db.session.query(User).filter(
        db.func.lower(User.name) != 'admin'
    ).count()
    data['total_page'] = user_num // per_page if user_num % per_page == 0 else user_num // per_page + 1
    db.session.remove()
    return render_template("admin_user.html", data=data)


@admin_view.route("/admin/delete_user", methods=['POST'])
def delete_user():
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return "error"
    user_id = request.form.get("id", None)
    if not user_id:
        return "error"
    try:
        user = db.session.query(User).filter(User.id == int(user_id)).one()
        db.session.query(UserCollection).filter(UserCollection.user_id == user.id).delete()
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return "error"
    finally:
        db.session.remove()
    return "success"


@admin_view.route("/admin/novels/<int:page>", methods=['GET'])
@admin_view.route("/admin/novels", methods=['GET'])
@error_processing
def admin_novels(page=1):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    per_page = 50
    data['current_page'] = page
    data['base_url'] = get_base_url_for_pagination(request.base_url, page)
    data['novels'] = db.session.query(NovelTitle).order_by(
        NovelTitle.id.asc()
    ).offset((page - 1) * per_page).limit(per_page)
    novels_num = db.session.query(NovelTitle).count()
    data['total_page'] = novels_num // per_page if novels_num % per_page == 0 else novels_num // per_page + 1
    db.session.remove()
    return render_template('admin_novel.html', data=data)


@admin_view.route("/admin/novels/sections", methods=['GET'])
@admin_view.route("/admin/novels/sections/<int:page>", methods=['GET'])
def admin_novels_order_by_section_num(page=1):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    per_page = 50
    data['current_page'] = page
    data['base_url'] = get_base_url_for_pagination(request.base_url, page)
    data['novels'] = db.session.query(
        NovelTitle
    ).outerjoin(NovelSection).group_by(NovelTitle.id).order_by(
        db.func.count(NovelSection.id).desc(),
        NovelTitle.id.asc()
    ).offset((page - 1) * per_page).limit(per_page)
    novels_num = db.session.query(NovelTitle).count()
    data['total_page'] = novels_num // per_page if novels_num % per_page == 0 else novels_num // per_page + 1
    db.session.remove()
    return render_template('admin_novel.html', data=data)


@admin_view.route("/admin/novels/heat", methods=['GET'])
@admin_view.route("/admin/novels/heat/<int:page>", methods=['GET'])
def admin_novels_order_by_heat(page=1):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    per_page = 50
    data['current_page'] = page
    data['base_url'] = get_base_url_for_pagination(request.base_url, page)
    data['novels'] = db.session.query(NovelTitle).order_by(
        NovelTitle.read_num.desc(),
        NovelTitle.id.asc()
    ).offset((page - 1) * per_page).limit(per_page)
    novels_num = db.session.query(NovelTitle).count()
    data['total_page'] = novels_num // per_page if novels_num % per_page == 0 else novels_num // per_page + 1
    db.session.remove()
    return render_template('admin_novel.html', data=data)


@admin_view.route("/admin/statistic/data", methods=['POST'])
@admin_view.route("/admin/statistic/data/<int:category_id>", methods=['POST'])
def admin_statistic_data(category_id=None):
    data_list = []
    if not category_id:
        for novel in db.session.query(NovelTitle).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(10):
            data_list.append({"read_num": novel.read_num, "id": novel.id, "name": novel.name})
    else:
        for novel in db.session.query(NovelTitle).filter(
            NovelTitle.type_id == category_id
        ).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(10):
            data_list.append({"read_num": novel.read_num, "id": novel.id, "name": novel.name})
    return jsonify(data_list)


@admin_view.route("/admin/statistic", methods=["GET"])
@error_processing
def admin_statistic():
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    db.session.remove()
    return render_template("admin_chart.html", data=data)


@admin_view.route("/admin/novel/<int:novel_id>/sections", methods=['GET'])
def admin_novel_sections(novel_id):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    data['novel_title'] = db.session.query(NovelTitle).filter(
        NovelTitle.id == novel_id
    ).one()
    data['sections'] = db.session.query(NovelSection).filter(
        NovelSection.novel_id == novel_id
    ).order_by(NovelSection.id.desc())
    db.session.remove()
    return render_template("admin_novel_sections.html", data=data)


@admin_view.route("/admin/novel/<int:novel_id>/addsection", methods=['GET', 'POST'])
def admin_add_novel_section(novel_id):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    if request.method == 'GET':
        data['novel'] = db.session.query(NovelTitle).filter(NovelTitle.id == novel_id).one()
        db.session.remove()
        return render_template("admin_add_novel_section.html", data=data)
    section_title = request.form.get("section_title", None)
    section_content = request.form.get("section_content", None)
    section_url = request.form.get("section_url", None)
    if not section_title or not section_content:
        return "error"
    section_content = '<br />'.join([x.strip() for x in section_content.split("\n")])
    try:
        db.session.add(NovelSection(
            novel_id=novel_id,
            title=section_title,
            content=section_content,
            url=section_url
        ))
        db.session.commit()
    except Exception as e:
        print(e)
        return "error"
    finally:
        db.session.remove()
    return "success"


@admin_view.route("/admin/novel/updateSection/<int:section_id>", methods=['GET', 'POST'])
def update_novel_section(section_id):
    if 'user' not in session or session['user']['name'].lower() != 'admin':
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    if request.method == 'GET':
        data['section'] = db.session.query(NovelSection).filter(NovelSection.id == section_id).one()
        data['section'].content = "\n".join(data['section'].content.split("<br />"))
        getattr(data['section'], 'novel_title', None)
        db.session.remove()
        return render_template("admin_update_novel_section.html", data=data)
    section_title = request.form.get("section_title", None)
    section_content = request.form.get("section_content", None)
    section_url = request.form.get("section_url", None)
    if not section_title or not section_content:
        return "error"
    section_content = '<br />'.join([x.strip() for x in section_content.split("\n")])
    try:
        db.session.query(NovelSection).filter(NovelSection.id == section_id).update(
            {
                NovelSection.title: section_title,
                NovelSection.content: section_content,
                NovelSection.url: section_url
            }
        )
        db.session.commit()
    except Exception as e:
        print(e)
        return "error"
    finally:
        db.session.remove()
    return "success"

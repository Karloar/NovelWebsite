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
def admin_statistic_data():
    data_list = []
    for novel in db.session.query(NovelTitle).order_by(NovelTitle.read_num.desc(), NovelTitle.id.asc()).limit(10):
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

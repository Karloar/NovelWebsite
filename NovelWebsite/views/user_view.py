from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from . import md5
from . import error_processing
from . import get_base_url_for_pagination
from ..models import db
from ..models import User
from ..models import UserCollection
from ..models import NovelType
from ..models import NovelTitle


user_view = Blueprint(__name__, 'user_view')


@user_view.route("/user/register", methods=['POST'])
def register():
    user_name = request.form.get('user_name', None)
    password = request.form.get('password', None)
    email = request.form.get('email', None)
    if not user_name or not password or not email:
        return 'fail'
    real_password = md5(password)
    try:
        db.session.query(User).filter(User.name == user_name, User.password == real_password).one()
    except Exception as e:
        print(e)
        db.session.add(User(name=user_name, password=real_password, email=email))
        db.session.commit()
        return 'success'
    finally:
        db.session.remove()
    return 'fail'


@user_view.route("/user/login", methods=['POST'])
def login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if not username or not password:
        return 'fail'
    try:
        user = db.session.query(User).filter(User.name == username, User.password == md5(password)).one()
        session['user'] = {"id": user.id, "name": user.name}
    except Exception as e:
        print(e)
        return 'fail'
    finally:
        db.session.remove()
    return 'success'


@user_view.route("/user/logout", methods=['POST'])
def logout():
    if 'user' in session:
        del session['user']
        return "success"
    return "error"


@user_view.route("/user/addCollection", methods=['POST'])
def add_collection():
    if 'user' not in session:
        return 'not_login'
    novel_id = request.form.get('novel_id', None)
    if not novel_id:
        return 'error'
    try:
        db.session.query(UserCollection).filter(
            UserCollection.user_id == session['user']['id'],
            UserCollection.novel_title_id == int(novel_id)
        ).one()
        return 'existed'
    except Exception as e:
        print(e)
        db.session.add(UserCollection(user_id=session['user']['id'], novel_title_id=int(novel_id)))
        db.session.commit()
        return 'success'
    finally:
        db.session.remove()
    return 'error'


@user_view.route("/user/collections/category/<int:category>/<int:page>", methods=['GET'])
@user_view.route("/user/collections/category/<int:category>", methods=['GET'])
@user_view.route("/user/collections/<int:page>", methods=['GET'])
@user_view.route("/user/collections", methods=['GET'])
@error_processing
def show_collections(page=1, category=None):
    if 'user' not in session:
        return redirect("/")
    data = dict()
    data['user'] = session['user']
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    per_page = 20
    data['base_url'] = get_base_url_for_pagination(request.base_url, page)
    data['current_page'] = page
    if category:
        data['collections'] = db.session.query(UserCollection).join(NovelTitle).filter(
            UserCollection.user_id == session['user']['id'],
            NovelTitle.type_id == category
        ).order_by(
            UserCollection.id.desc(),
            NovelTitle.read_num.desc(),
            NovelTitle.id.asc()
        ).offset((page - 1) * per_page).limit(per_page)
        collection_num = db.session.query(UserCollection).join(NovelTitle).filter(
            UserCollection.user_id == session['user']['id'],
            NovelTitle.type_id == category
        ).count()
    else:
        data['collections'] = db.session.query(UserCollection).join(NovelTitle).filter(
            UserCollection.user_id == session['user']['id'],
        ).order_by(
            UserCollection.id.desc(),
            NovelTitle.read_num.desc(),
            NovelTitle.id.asc()
        ).offset((page - 1) * per_page).limit(per_page)
        collection_num = db.session.query(UserCollection).join(NovelTitle).filter(
            UserCollection.user_id == session['user']['id'],
        ).count()
    data['total_page'] = collection_num // per_page if collection_num % per_page == 0 else collection_num // per_page + 1
    db.session.remove()
    return render_template("collection.html", data=data)


@user_view.route("/user/removeCollection", methods=['POST'])
def remove_collection():
    collection_id = request.form.get('collection_id', None)
    if not collection_id:
        return 'error'
    try:
        collection = db.session.query(UserCollection).filter(UserCollection.id == int(collection_id)).one()
        db.session.delete(collection)
        db.session.commit()
    except Exception as e:
        print(e)
        return 'error'
    finally:
        db.session.remove()
    return 'success'



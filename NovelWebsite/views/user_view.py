from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from . import md5
from ..models import db
from ..models import User
from ..models import UserCollection


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


@user_view.route("/user/logout", methods=['GET'])
def logout():
    if 'user' in session:
        del session['user']
    return redirect("/")


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

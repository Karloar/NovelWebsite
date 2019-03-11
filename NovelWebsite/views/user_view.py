from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from . import md5
from ..models import db
from ..models import User


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

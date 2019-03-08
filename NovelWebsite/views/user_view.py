from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from . import md5


user_view = Blueprint(__name__, 'user_view')


@user_view.route("/user/register", methods=['POST'])
def register():
    pass

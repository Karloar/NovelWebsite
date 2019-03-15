from flask import Flask
from .models import db
from .views.index_view import index_view
from .views.user_view import user_view
from .views.admin_view import admin_view


def create_app():
    app = Flask(__name__)
    # register config file
    app.config.from_object("settings.Config")
    # register blue_print
    app.register_blueprint(index_view)
    app.register_blueprint(user_view)
    app.register_blueprint(admin_view)
    # register database config from app config
    db.init_app(app)
    return app

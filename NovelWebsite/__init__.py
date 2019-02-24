from flask import Flask
from .models import db


def create_app():
    app = Flask(__name__)
    # register config file
    app.config.from_object("settings.Config")
    # register blue_print
    # app.register_blueprint()
    # register database config from app config
    db.init_app(app)
    return app

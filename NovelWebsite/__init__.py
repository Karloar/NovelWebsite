from flask import Flask
from flask import render_template
from .models import db

def index():
    return render_template("index.html", name='张三')

def create_app():
    app = Flask(__name__)
    # register config file
    app.config.from_object("settings.Config")
    app.add_url_rule("/", view_func=index)
    # register blue_print
    # app.register_blueprint()
    # register database config from app config
    db.init_app(app)
    return app

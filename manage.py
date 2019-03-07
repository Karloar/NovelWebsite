from flask import render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_migrate import MigrateCommand
from flask_migrate import Migrate
from NovelWebsite.models import db
from NovelWebsite.models import NovelType
from NovelWebsite import create_app


app = create_app()
bootstrap = Bootstrap(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.errorhandler(404)
def error_404(error):
    data = dict()
    data['type_list'] = db.session.query(NovelType).order_by(NovelType.id)
    db.session.remove()
    return render_template("error_404.html", data=data)


if __name__ == '__main__':
    manager.run()

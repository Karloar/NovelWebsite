from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_migrate import MigrateCommand
from flask_migrate import Migrate
from NovelWebsite.models import db
from NovelWebsite import create_app


app = create_app()
bootstrap = Bootstrap(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

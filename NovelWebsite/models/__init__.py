from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(30))
    email = db.Column(db.String(100))
    user_collections = db.relationship("UserCollection", backref="user", lazy='dynamic')


class UserCollection(db.Model):
    __tablename__ = 'user_collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    novel_title_id = db.Column(db.Integer, db.ForeignKey("novel_title.id"))


class NovelTitle(db.Model):
    __tablename__ = 'novel_title'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    cover = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    introduction = db.Column(db.String(200))
    url = db.Column(db.String(200), unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey("novel_type.id"))
    read_num = db.Column(db.Integer, default='0')
    novel_sections = db.relationship("NovelSection", backref="novel_title", lazy='dynamic')
    user_collections = db.relationship("UserCollection", backref="novel_title", lazy='dynamic')


class NovelSection(db.Model):
    __tablename__ = 'novel_section'
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey("novel_title.id"))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    url = db.Column(db.String(100), unique=True)

    __table_args__ = {
        'mysql_charset': 'utf8mb4'
    }


class CrawlSettings(db.Model):
    __tablename__ = 'crawl_settings'
    id = db.Column(db.Integer, primary_key=True)
    crawl_time = db.Column(db.DateTime)


class NovelType(db.Model):
    __tablename__ = 'novel_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    novel_titles = db.relationship("NovelTitle", backref="novel_type", lazy='dynamic')

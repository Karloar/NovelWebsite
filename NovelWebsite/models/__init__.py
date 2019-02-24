from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(30))


class UserCollection(db.Model):
    __tablename__ = 'user_collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))



class NovelTitle(db.Model):
    __tablename__ = 'novel_title'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))


class NovelSection(db.Model):
    __tablename__ = 'novel_section'
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey("novel_title.id"))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)


class CrawlSettings(db.Model):
    __tablename__ = 'crawl_settings'
    id = db.Column(db.Integer, primary_key=True)
    crawl_time = db.Column(db.DateTime)

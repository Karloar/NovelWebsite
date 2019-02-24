from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)


class NovelTitle(db.Model):
    __tablename__ = 'novel_title'
    id = db.Column(db.Integer, primary_key=True)


class NovelSection(db.Model):
    __tablename__ = 'novel_section'
    id = db.Column(db.Integer, primary_key=True)


class CrawlSettings(db.Model):
    __tablename__ = 'crawl_settings'
    id = db.Column(db.Integer, primary_key=True)

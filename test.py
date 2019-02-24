from NovelWebsite.models import db
from NovelWebsite.models import CrawlSettings
from manage import app
from datetime import datetime


if __name__ == '__main__':
    db.app = app
    db.session.add(CrawlSettings(crawl_time=datetime.now()))
    db.session.commit()
    db.session.remove()

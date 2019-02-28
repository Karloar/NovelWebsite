from datetime import datetime
from NovelSpider import get_novel_titles_from_url
from NovelSpider import db
from NovelSpider import NovelTitle
from NovelSpider import NovelType


base_url = "http://www.shuquge.com/category/1_1.html"


if __name__ == '__main__':
    today = datetime.now().strftime("%Y-%m-%d")
    type_id = db.session.query(NovelType).filter(NovelType.name == '都市言情').one().id
    i = 1
    flag = True
    while flag:
        url = "http://www.shuquge.com/category/{0}_{1}.html".format(type_id, str(i))
        for novel_title in get_novel_titles_from_url(url):
            print(novel_title.name)
            if not today.endswith(novel_title.update_date):
                flag = False
                break
            novel_title.type_id = type_id
            try:
                db.session.query(NovelTitle).filter(NovelTitle.url == novel_title.url).one()
            except Exception as e:
                db.session.add(novel_title)
                db.session.commit()
        i += 1
    db.session.remove()



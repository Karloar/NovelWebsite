from NovelWebsite.models import db
from NovelWebsite.models import NovelType
from manage import app


db.app = app


if __name__ == '__main__':
    type_list = ['玄幻魔法', '武侠修真', '都市言情', '历史军事', '侦探推理', '网游动漫', '科幻灵异', '其他类型']
    db.app = app
    for t in type_list:
        db.session.add(NovelType(name=t))
    db.session.commit()
    db.session.remove()

import os
from NovelSpider.utils import CrawlNovelSectionThread
from NovelSpider import db
from NovelSpider import NovelTitle
from NovelSpider import NovelType


cover_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'NovelWebsite',
    'static',
    'img',
    'cover'
)


novel_type_list = ['玄幻魔法', '武侠修真', '都市言情', '历史军事', '侦探推理', '网游动漫', '科幻灵异', '其他类型']


if __name__ == '__main__':
    for novel_type in novel_type_list:
        novel_type_obj = db.session.query(NovelType).filter(NovelType.name == novel_type).one()
        novel_title_list = db.session.query(NovelTitle).filter(NovelTitle.novel_type == novel_type_obj).all()
        CrawlNovelSectionThread(novel_title_list, cover_path, lock=True).start()

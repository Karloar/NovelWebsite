import os
from NovelSpider import download_cover
from NovelSpider import db
from NovelSpider import NovelTitle
from NovelSpider.utils import get_cover_href_from_url
from NovelSpider.utils import get_introduction_from_title_url

cover_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'NovelWebsite',
    'static',
    'img',
    'cover'
)


if __name__ == '__main__':
    for novel_title in db.session.query(NovelTitle).all():
        cover_file_name = os.path.join(cover_path, str(novel_title.id) + '.jpg')
        if novel_title.cover is None or not os.path.exists(cover_file_name):
            cover_src = get_cover_href_from_url(novel_title.url)
            download_cover(cover_src, cover_file_name)
            novel_title.cover = '/static/img/cover/{0}.jpg'.format(str(novel_title.id))
            db.session.query(NovelTitle).filter(NovelTitle.id == novel_title.id).update(
                {NovelTitle.cover: novel_title.cover}
            )
            db.session.commit()
            print(novel_title.id, '  ', novel_title.name, '  ', novel_title.url, '  ', cover_src)
        if novel_title.introduction is None:
            novel_title.introduction = get_introduction_from_title_url(novel_title.url)
            db.session.query(NovelTitle).filter(NovelTitle.id == novel_title.id).update(
                {NovelTitle.introduction: novel_title.introduction}
            )
            db.session.commit()
            print(novel_title.id, '  ', novel_title.name, '  ', novel_title.url)

    db.session.remove()

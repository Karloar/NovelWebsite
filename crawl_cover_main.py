import os
from NovelSpider import download_cover
from NovelSpider import db
from NovelSpider import NovelTitle
from NovelSpider.utils import get_cover_href_from_url


cover_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'NovelWebsite',
    'static',
    'img',
    'cover'
)


if __name__ == '__main__':
    for novel_title in db.session.query(NovelTitle).all():
        if novel_title.cover is None:
            cover_src = get_cover_href_from_url(novel_title.url)
            cover_file_name = os.path.join(cover_path, str(novel_title.id) + '.jpg')
            download_cover(cover_src, cover_file_name)
            novel_title.cover = '/static/img/cover/{0}.jpg'.format(str(novel_title.id))
            db.session.query(NovelTitle).filter(NovelTitle.id == novel_title.id).update(
                {NovelTitle.cover: novel_title.cover}
            )
            db.session.commit()
            print(novel_title.id, '  ', novel_title.name, '  ', novel_title.url, '  ', cover_src)
    db.session.remove()

from NovelSpider.utils import get_section_content_from_url
from NovelSpider.utils import NovelSection
from NovelSpider.utils import get_section_title_and_url_from_title_url
from NovelSpider.utils import NovelTitle
from NovelSpider.utils import db


if __name__ == '__main__':
    novel_title = db.session.query(NovelTitle).filter(NovelTitle.name == '元尊').one()
    try:
        section_title_and_url_list = get_section_title_and_url_from_title_url(novel_title.url)
        for title, url in section_title_and_url_list:
            try:
                db.session.query(NovelSection).filter(NovelSection.url == url).one()
            except:
                try:
                    content = get_section_content_from_url(url)
                    db.session.add(NovelSection(
                        novel_id=novel_title.id,
                        title=title,
                        content=content.encode('utf-8'),
                        url=url
                    ))
                    db.session.commit()
                    print(novel_title.id, '  ', novel_title.name, '  ', title, '  ', url)
                    # time.sleep(1)
                except Exception as e:
                    print(e)
                    break
    except Exception as e:
        print(e, '  ', novel_title.url)


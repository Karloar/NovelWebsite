import threading
import requests
from lxml import etree
from datetime import datetime
from NovelSpider import db
from NovelSpider import NovelType
from NovelSpider import NovelTitle


def get_novel_titles_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    li_list = selector.xpath("/html/body/div[4]/div[2]/div[1]/ul/li")
    novel_title_list = []
    for li in li_list:
        title = str(li.xpath("span[2]/a/text()")[0]).strip()
        href = str(li.xpath("span[2]/a/@href")[0]).strip()
        author = str(li.xpath("span[4]/text()")[0]).strip()
        date = str(li.xpath("span[5]/text()")[0]).strip()
        novel_title = NovelTitle(name=title, author=author, url=href)
        novel_title.update_date = date
        novel_title_list.append(novel_title)
    return novel_title_list


class CrawlNovelTitleThread(threading.Thread):

    def __init__(
            self,
            novel_type,
            base_url='http://www.shuquge.com/category/',
            date=datetime.today().strftime('%Y-%m-%d')
    ):
        threading.Thread.__init__(self)
        self.__novel_type_id = db.session.query(NovelType).filter(NovelType.name == novel_type).one().id
        self.__base_url = base_url
        self.__date = date

    def run(self):
        page = 1
        is_crawl = True
        while is_crawl:
            crawl_url = "{base}{type_id}_{page}.html".format(
                base=self.__base_url,
                type_id=self.__novel_type_id,
                page=page
            )
            for novel_title in get_novel_titles_from_url(crawl_url):
                if not self.__date.endswith(novel_title.update_date):
                    is_crawl = False
                    break
                novel_title.type_id = self.__novel_type_id
                try:
                    db.session.query(NovelTitle).filter(NovelTitle.url == novel_title.url).one()
                except:
                    db.session.add(novel_title)
                    db.session.commit()
                    print(threading.current_thread().getName(), '  ', novel_title.name, '  ', novel_title.url)
            page += 1
        db.session.remove()


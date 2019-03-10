import threading
import requests
import html
import time
from lxml import etree
from datetime import datetime
from NovelSpider import db
from NovelSpider import NovelType
from NovelSpider import NovelTitle
from NovelSpider import NovelSection


def get_novel_titles_from_url(url):
    '''
    从url中找到所有的小说标题
    :param url:
    :return:
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    try:
        novel_title_list = []
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        selector = etree.HTML(resp.text)
        li_list = selector.xpath("/html/body/div[4]/div[2]/div[1]/ul/li")

        for li in li_list:
            title = str(li.xpath("span[2]/a/text()")[0]).strip()
            href = str(li.xpath("span[2]/a/@href")[0]).strip()
            author = str(li.xpath("span[4]/text()")[0]).strip()
            date = str(li.xpath("span[5]/text()")[0]).strip()
            novel_title = NovelTitle(name=title, author=author, url=href)
            novel_title.update_date = date
            novel_title_list.append(novel_title)
    except Exception as e:
        print(e)
    return novel_title_list


def get_section_title_and_url_from_title_url(title_url):
    '''
    从当前小说页面获取所有的章节
    :param title_url:
    :return:
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    base_url, _ = title_url.rsplit("/", maxsplit=1)
    resp = requests.get(title_url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    sections = selector.xpath("/html/body/div[5]/dl/dt[2]/following-sibling::*")
    title_and_url_list = []
    for section in sections:
        title_node = section.xpath("./a/text()")
        href_node = section.xpath("./a/@href")
        if len(title_node) == 0 or len(href_node) == 0:
            continue
        title = str(title_node[0])
        href = base_url + "/" + str(href_node[0])
        title_and_url_list.append((title, href))
    return title_and_url_list


def get_title_from_title_url(title_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(title_url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    name = selector.xpath("/html/body/div[4]/div[2]/h2/text()")[0]
    type_name = selector.xpath("/html/body/div[4]/div[2]/div[2]/span[2]/text()")[0].split("：")[-1]
    author = selector.xpath("/html/body/div[4]/div[2]/div[2]/span[1]/text()")[0].split("：")[-1]
    novel_title = NovelTitle(
        name=name,
        author=author,
        url=title_url,
        type_id=db.session.query(NovelType).filter(NovelType.name == type_name).one().id
    )
    return novel_title


def get_cover_href_from_url(url):
    '''
    从小说title url中找到封面的url
    :param url:
    :return:
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    cover_src = selector.xpath("/html/body/div[4]/div[2]/div[1]/img/@src")
    return str(cover_src[0])


def get_introduction_from_title_url(url):
    '''
    从小说title url中找到简介
    :param url:
    :return:
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    introduction = selector.xpath("/html/body/div[4]/div[2]/div[3]/text()")[:-1]
    introduction = [html.escape(x).strip() for x in introduction if x.strip()]
    return '<br />'.join(introduction)


def download_cover(cover_src, file_name, chunk_size=None):
    '''
    下载封面到指定目录
    :param cover_src:
    :param file_name:
    :param chunk_size:
    :return:
    '''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(url=cover_src, stream=True, headers=headers)
    with open(file_name, 'wb') as f:
        if chunk_size and type(chunk_size) == int:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                f.write(chunk)
        else:
            f.write(resp.content)


def get_section_content_from_url(section_url):
    '''
    根据章节
    :param section_url:
    :return:
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }

    resp = requests.get(url=section_url, headers=headers)
    resp.encoding = "utf-8"
    selector = etree.HTML(resp.text)
    contents = selector.xpath('//*[@id="content"]/text()')
    contents = [html.escape(x).strip() for x in contents if x.strip()]
    return '<br />'.join(contents)


content_lock = threading.Lock()


class CrawlNovelTitleThread(threading.Thread):
    '''
    下载小说标题的线程类
    '''

    def __init__(
            self,
            novel_type,
            base_url='http://www.shuquge.com/category/',
            date=datetime.today().strftime('%Y-%m-%d'),
            max_error_page=5
    ):
        threading.Thread.__init__(self)
        self.__novel_type_id = db.session.query(NovelType).filter(NovelType.name == novel_type).one().id
        self.__base_url = base_url
        self.__date = date
        self.__max_error_page = max_error_page

    def run(self):
        page = 1
        is_crawl = True
        error_page = 0
        while is_crawl:
            crawl_url = "{base}{type_id}_{page}.html".format(
                base=self.__base_url,
                type_id=self.__novel_type_id,
                page=page
            )
            novel_title_list = get_novel_titles_from_url(crawl_url)
            if len(novel_title_list) == 0:
                error_page += 1
            if error_page >= self.__max_error_page:
                break
            for novel_title in novel_title_list:
                if not self.__date.endswith(novel_title.update_date):
                    continue
                novel_title.type_id = self.__novel_type_id
                try:
                    db.session.query(NovelTitle).filter(NovelTitle.url == novel_title.url).one()
                except:
                    db.session.add(novel_title)
                    db.session.commit()
                    print(threading.current_thread().getName(), '  ', novel_title.name, '  ', novel_title.url)
            page += 1
        db.session.remove()


class CrawlNovelSectionThread(threading.Thread):
    '''
    下载小说章节的线程, 若没有下载小说封面, 下载小说封面
    '''
    def __init__(self, novel_title_list: NovelTitle, lock=False, ignore_list=None):
        threading.Thread.__init__(self)
        self.__novel_title_list = novel_title_list
        self.__lock = lock
        self.__ignore_list = ignore_list

    def run(self):
        for novel_title in self.__novel_title_list:
            if self.__ignore_list and novel_title.id in self.__ignore_list:
                continue
            try:
                section_title_list = get_section_title_and_url_from_title_url(novel_title.url)
                for section_title, section_url in section_title_list:
                    if content_lock.acquire():
                        try:
                            db.session.query(NovelSection).filter(NovelSection.url == section_url).one()
                        except Exception as _:
                            # print(e)
                            try:
                                section_content = get_section_content_from_url(section_url)
                                db.session.add(NovelSection(
                                    title=section_title,
                                    content=section_content.encode('utf-8'),
                                    url=section_url,
                                    novel_id=novel_title.id
                                ))
                                db.session.commit()
                                print(threading.current_thread().getName(), '  ', novel_title.id, '  ',
                                      novel_title.name, '  ', section_title, '  ', section_url)
                            except Exception as e:
                                print(e)
                                db.session.remove()
                                break
                        finally:
                            content_lock.release()

            except Exception as e:
                print(e, '  ', novel_title.url)
        db.session.remove()

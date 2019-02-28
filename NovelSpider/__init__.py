import requests
from lxml import etree
from NovelWebsite.models import db
from NovelWebsite.models import NovelTitle
from NovelWebsite.models import NovelType
from NovelWebsite.models import NovelSection
from manage import app


db.app = app


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


def get_section_title_and_url_from_titl_url(title_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    base_url, _ = title_url.rsplit("/", maxsplit=1)
    resp = requests.get(title_url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    sections = selector.xpath("/html/body/div[5]/dl/dt[last()]/following-sibling::*")
    title_and_url_list = []
    for section in sections:
        title = str(section.xpath("./a/text()")[0])
        href = base_url + "/" + str(section.xpath("./a/@href")[0])
        if not (title.startswith("正文") or title.startswith("第")):
            continue
        title_and_url_list.append((title, href))
    return title_and_url_list

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


def get_section_title_and_url_from_title_url(title_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    base_url, _ = title_url.rsplit("/", maxsplit=1)
    resp = requests.get(title_url, headers=headers)
    resp.encoding = 'utf-8'
    selector = etree.HTML(resp.text)
    sections = selector.xpath("/html/body/div[5]/dl/dt[2]/following-sibling::*")
    cover_src = selector.xpath("/html/body/div[4]/div[2]/div[1]/img/@src")
    title_and_url_list = []
    for section in sections:
        title_node = section.xpath("./a/text()")
        href_node = section.xpath("./a/@href")
        if len(title_node) == 0 or len(href_node) == 0:
            continue
        title = str(title_node[0])
        href = base_url + "/" + str(href_node[0])
        title_and_url_list.append((title, href))
    return title_and_url_list, str(cover_src[0])


def download_cover(img_src, file_name, chunk_size=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(url=img_src, stream=True, headers=headers)
    with open(file_name, 'wb') as f:
        if chunk_size and type(chunk_size) == int:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                f.write(chunk)
        else:
            f.write(resp.content)

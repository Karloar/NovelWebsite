from NovelSpider import get_section_title_and_url_from_titl_url
from NovelSpider import download_cover
from NovelSpider import db
from NovelSpider import NovelTitle
import requests
from lxml import etree
from lxml.html import tostring
import html
import os


cover_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'NovelWebsite',
    'static',
    'img',
    'covers'
)


url = "http://www.shuquge.com/txt/5809/index.html"
url = "http://www.shuquge.com/txt/85748/index.html"
url = "http://www.shuquge.com/txt/8659/index.html"
url = "http://www.shuquge.com/txt/8659/23051838.html"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
}

resp = requests.get(url=url, headers=headers)
resp.encoding = "utf-8"
selector = etree.HTML(resp.text)
div = selector.xpath('//*[@id="content"]')[0]
content = etree.tostring(div, pretty_print=False, method='html')
# content = content.replace("请记住本书首发域名：www.shuquge.com。书趣阁_笔趣阁手机版阅读网址：m.shuquge.com", "")
print(type(content))
print(html.unescape(str(content)))

# for novel_title in db.session.query(NovelTitle).all():
#     if novel_title.cover is None:
#         section_title_and_url_list, cover_src = get_section_title_and_url_from_titl_url(novel_title.url)
#         cover_file_name = os.path.join(cover_path, str(novel_title.id) + '.jpg')
#         download_cover(cover_src, cover_file_name)
#         novel_title.cover = '/static/img/cover/{0}.jpg'.format(str(novel_title.id))
#         db.session.query(NovelTitle).filter(NovelTitle.id == novel_title.id).update({NovelTitle.cover: novel_title.cover})
#         db.session.commit()
# db.session.remove()





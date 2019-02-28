from NovelSpider import get_section_title_and_url_from_titl_url
import requests
from lxml import etree
from lxml.html import tostring
import html


url = "http://www.shuquge.com/txt/5809/index.html"
url = "http://www.shuquge.com/txt/85748/index.html"
url = "http://www.shuquge.com/txt/8659/index.html"
url = "http://www.shuquge.com/txt/8659/23051838.html"
#
#
# for title, url in get_section_title_and_url_from_titl_url(url):
#     print(title, url)
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

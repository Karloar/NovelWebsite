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


# def get_novel_by_name(db, name):
#     novel = db.session.query(NovelType).filter(NovelType.name == name).one()
#     db.session.remove()
#     return novel.id
# # if __name__ == '__main__':
# #     type_list = ['玄幻魔法', '武侠修真', '都市言情', '历史军事', '侦探推理', '网游动漫', '科幻灵异', '其他类型']
# #     db.app = app
# #     for type in type_list:
# #         db.session.add(NovelType(name=type))
# #     db.session.commit()
# #     db.session.remove()
# #     print(get_novel_by_name('武侠修真'))

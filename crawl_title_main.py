from NovelSpider.utils import CrawlNovelTitleThread


novel_type_list = ['玄幻魔法', '武侠修真', '都市言情', '历史军事', '侦探推理', '网游动漫', '科幻灵异', '其他类型']


if __name__ == '__main__':
    for novel_type in novel_type_list:
        CrawlNovelTitleThread(novel_type).start()

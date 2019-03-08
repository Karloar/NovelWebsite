import hashlib
from flask import abort
from functools import wraps
from settings import Config


def error_processing(process_func):
    '''
    包裹视图函数, 若出现异常直接返回404信息
    :param process_func:
    :return:
    '''
    @wraps(process_func)
    def inner_function(*args, **kwargs):
        try:
            value = process_func(*args, **kwargs)
        except Exception as e:
            print(e)
            abort(404)
        return value
    return inner_function


def md5(message):
    m2 = hashlib.md5(Config.MD5_KEY.encode('utf-8'))
    m2.update(message.encode('utf-8'))
    return m2.hexdigest()


# def get_page_label_range(current_page, total_page, page_r=3):
#     page_label_num = 2 * page_r + 1
#     if total_page <= page_label_num:
#         return range(1, total_page+1)
#     if current_page <= page_r:
#         return range(1, page_label_num+1)
#     if current_page + page_r >= total_page:
#         return range(total_page - page_label_num+1, total_page+1)
#     return range(current_page-page_r, current_page+page_r+1)

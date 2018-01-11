#! coding: utf-8
"""
用于存放urllib相关操作方法
2018年1月11日 15:42:30
"""
from urllib import request, parse


def get_url_act(url):
    return eval(request.urlopen(url).read())


def post_url_act(url, data):
    data = parse.urlencode(data)
    req = request.Request(url, data=data)
    return eval(request.urlopen(req).read())
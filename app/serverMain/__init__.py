# coding:utf-8
from flask import Blueprint

serverMain = Blueprint('serverMain', __name__)

from app.serverMain import views

from . import forms
# 由于路由和错误处理页面定义在这个文件里面，导入到蓝本把他们关联起来
# 又因为views.py，error.py需要导入蓝本main，防止循环导入所以放到最后
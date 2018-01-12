#! coding:utf-8
from app import db
from flask_login import UserMixin
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    passwd = db.Column(db.String(64))
    email = db.Column(db.String(64))
    token = db.Column(db.String(64))
    level = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    # flask-login 需要实现的回调函数
    return User.query.get(int(user_id))


class SpiderLog(db.Model):
    __tablename__ = 'spider_log'
    id = db.Column(db.Integer, primary_key=True)
    spiderName = db.Column(db.String(20), index=True)
    startTime = db.Column(db.String(64))
    endTie = db.Column(db.String(64))
    initiator = db.Column(db.String(64))    # 启动爬虫的用户
    errorNum = db.Column(db.Integer)    # 错误数量
    isEnd = db.Column(db.Integer)       # 是否非正常关闭


class ScrapyProject(db.Model):
    __tablename__ = 'scrapy_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    spider_count = db.Column(db.Integer)        # 该项目下爬虫总数
    introduce = db.Column(db.Text)              # 项目简介
    create_time = db.Column(db.DateTime)


class SpiderInfo(db.Model):
    __tablename__ = 'spider_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    sp_url = db.Column(db.String(120))          # 该爬虫的url
    run_count = db.Column(db.Integer)           # 工作次数
    item_count = db.Column(db.Integer)          # 爬取的item数量
    url_count = db.Column(db.Integer)           # 爬取的页面数量
    introduce = db.Column(db.Text)              # 爬虫简介
    project_id = db.Column(db.Integer)          # 所属项目组ID
    create_time = db.Column(db.DateTime)
#! coding:utf-8
from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    userpwd = db.Column(db.String(64))
    token = db.Column(db.String(64))
    level = db.Column(db.Integer)


class SpiderLog(db.Model):
    __tablename__ = 'spider_log'
    id = db.Column(db.Integer, primary_key=True)
    spiderName = db.Column(db.String(20), index=True)
    startTime = db.Column(db.String(64))
    endTie = db.Column(db.String(64))
    initiator = db.Column(db.String(64))    # 启动爬虫的用户
    errorNum = db.Column(db.Integer)    # 错误数量
    isEnd = db.Column(db.Integer)       # 是否非正常关闭


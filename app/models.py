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


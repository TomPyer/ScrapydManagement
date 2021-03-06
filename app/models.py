#! coding:utf-8
from app import db, login_manager
from flask_login import UserMixin
from utils.crypt import signature, des_encrypt, gen_md5_salt


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    passwd = db.Column(db.String(64))
    email = db.Column(db.String(64))
    token = db.Column(db.String(64))
    project_count = db.Column(db.Integer)
    spider_count = db.Column(db.Integer)
    task_count = db.Column(db.Integer)
    level_num = db.Column(db.Integer)
    level = db.Column(db.String(20))
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


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
    create_person = db.Column(db.String(30))
    create_time = db.Column(db.DateTime)
    node_name = db.Column(db.String(30))
    version = db.Column(db.String(20))


class SpiderInfoDB(db.Model):
    __tablename__ = 'spider_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    sp_url = db.Column(db.String(120))          # 该爬虫的url
    status = db.Column(db.String(20))           # 当前状态
    run_time = db.Column(db.Integer)            # 当前状态持续时间
    run_count = db.Column(db.Integer)           # 工作次数
    item_count = db.Column(db.Integer)          # 爬取的item数量
    url_count = db.Column(db.Integer)           # 爬取的页面数量
    introduce = db.Column(db.Text)              # 爬虫简介
    project = db.Column(db.String(20))             # 所属项目组
    version = db.Column(db.String(20))
    create_person = db.Column(db.String(30))
    create_time = db.Column(db.DateTime)


class OperaLog(db.Model):
    __tablename__ = 'opera_log'
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50))        # 操作名称
    operation_name = db.Column(db.String(50))   # 被操作对象名称
    person = db.Column(db.String(50))           # 执行人
    create_time = db.Column(db.DateTime)


class TaskInfo(db.Model):
    __tablename__ = 'task_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    work_num = db.Column(db.Integer)
    content = db.Column(db.String(200))
    create_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(50))
    status = db.Column(db.String(20))
    introduce = db.Column(db.String(20))
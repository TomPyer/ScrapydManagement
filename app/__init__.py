#! coding:utf-8
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def app_create(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]) # 可以直接把对象里面的配置数据转换到app.config里面
    config[config_name].init_app(app)

    bootstrap.app_init(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # 路由和其他处理程序定义
    # ...
    from app.scdMain import scdMain as scd_blueprint
    app.register_blueprint(scd_blueprint, url_prefix='/scd')

    return app
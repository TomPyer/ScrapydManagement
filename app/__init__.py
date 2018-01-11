#! coding:utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # None/basic/strong 代表不同的安全等级
login_manager.login_view = 'scdMain.login'   # 定义login view,在login_required装饰器中用到


def app_create(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 可以直接把对象里面的配置数据转换到app.config里面
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 该参数默认为None并会弹出警告
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True          # 启用本地cdn
    app.config.update(MAIL_SERVER='smtp.qq.com',
                    MAIL_PROT=25,
                    MAIL_USE_TLS=True,
                    MAIL_USE_SSL=False,
                    MAIL_USERNAME="271348762@qq.com",
                    MAIL_PASSWORD="byytrmvwmtwzbhgh",
                    MAIL_DEBUG=True)
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # 路由和其他处理程序定义
    # ...
    from app.scdMain import scdMain as scd_blueprint
    app.register_blueprint(scd_blueprint, url_prefix='/scdMain')

    return app
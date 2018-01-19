import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        # 执行当前环境的初始化操作
        pass


class DevelopmentConfig(Config):
    # 开发环境
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # scrapyd相关API
    SCRAPYD_URL = 'http://127.0.0.1:6800/'
    GET_PROJECTS_URL = 'http://127.0.0.1:6800/listprojects.json'
    GET_SPIDERS_URL = 'http://127.0.0.1:6800/listspiders.json'
    GET_SPIDER_BAT_URL = 'http://127.0.0.1:6800/listversions.json'
    GET_PROJECT_TASK = 'http://127.0.0.1:6800/listjobs.json'
    GET_PROJECT_JOBS_INFO = 'http://127.0.0.1:6800/listjobs.json'
    DEL_PROJECT_URL = 'http://127.0.0.1:6800/delproject.json'
    DEL_PROJECT_VER_URL = 'http://127.0.0.1:6800/delversion.json'
    STOP_SPIDER_URL = 'http://127.0.0.1:6800/cancel.json'
    START_SPIDER_URL = 'http://127.0.0.1:6800/schedule.json'

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = '6379'

    # scrapy目录配置
    SCRAPYPWD = 'D:\work\scrapyPython3'


class TestingConfig(Config):
    # 测试环境
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    # 生产环境
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
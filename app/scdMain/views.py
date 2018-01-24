#! coding:utf-8
from app.scdMain import scdMain                                 # 自定义app
from flask import render_template, request, redirect, url_for, flash, current_app   # 基础内容
from app.models import User, SpiderLog, db                      # 模板内容
from utils.crypt import signature, des_encrypt, gen_md5_salt    # 加密函数
from flask_login import login_required, logout_user             # 路由保护
from app.scdMain.forms import LoginForm, RegisterForm
from flask_mail import Message
from app.models import ScrapyProject, SpiderInfoDB, SpiderLog, OperaLog
from app import mail, db

import traceback
import subprocess
from datetime import datetime
import os
from .spiderinfo import SpiderInfo


@scdMain.route('/register', methods=['GET', 'POST'])
def register():
    # 注册
    if request.method == 'POST':
        try:
            token = gen_md5_salt()
            user_obj = User(username=signature(request.form.get('username'), 'tangxl66'),
                            passwd=des_encrypt(request.form.get('password'), token), token=token,
                            email=request.form.get('email'), level=0)
            db.session.add(user_obj)
            db.session.commit()
            return render_template('index.html')
        except Exception as e:
            print(e)
            traceback.print_exc()
    else:
        form = RegisterForm()
        return render_template('register.html', form=form)


@scdMain.route('/login', methods=['POST', 'GET'])
def login():
    # 登录
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if valid_login(request.form['email'],
                       request.form['password']):
            return log_the_user_in(request.form['email'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error, form=form)


@scdMain.route('/logout')
@login_required
def logout():
    # 登出
    logout_user()
    return redirect(url_for('/login'))


def valid_login(email, pwd):
    # 验证账号密码
    us_obj = User.query.filter_by(email=email).first()
    if us_obj:
        token = us_obj.token
        pwd = des_encrypt(pwd, token)
        if pwd == us_obj.passwd:
            return True
        else:
            return False
    else:
        return False


def log_the_user_in(user):
    # 登录后的操作, 登录系统暂时不完整, 以后再写
    return render_template('index.html')


@scdMain.route('/index', methods=['GET', 'POST'])
@scdMain.route('/', methods=['GET', 'POST'])
def index():
    # 首页
    return render_template('index.html')


@scdMain.route('/contact', methods=['GET'])
def contact():
    # 登录/注册页面
    return render_template('contact.html')


@scdMain.route('/work', methods=['GET'])
def work():
    """
    工作首页
    需要展示所有项目概览图和名称
    """
    spi_obj = SpiderInfo()
    project_info = spi_obj.get_scrapy_project_info()
    project_count = spi_obj.projects_count
    project_spider_count = spi_obj.spiders_count
    return render_template('work.html', project_dic=project_info, project_count=project_count,
                           project_spider_count=project_spider_count)


@scdMain.route('/message', methods=['POST'])
def message():
    # 网页信息发送至开发者邮箱
    msg = Message(request.form['msg_body'], sender='271348762@qq.com', recipients=['zenmeshenmedoubang@qq.com'])
    msg.body = request.form['msg_body']
    mail.send(msg)
    return render_template('contact.html')


@scdMain.route('/apsched', methods=['GET'])
def apsched():
    return render_template('apsched.html')


@scdMain.route('/fla', methods=['GET'])
def fla():
    flash('lalalalalalaal', 'warning')
    return render_template('flash.html')


@scdMain.route('/create_project', methods=['POST'])
def create_prject():
    # 创建项目
    if request.method == 'POST':
        try:
            subprocess.Popen(['scrapy', 'startproject', request.form['name']], cwd='D:\work\scrapyProject')
            dirs = 'D:\work\scrapyProject\%s\scrapy.cfg' % request.form['name']
            flag = True
            now = datetime.now()
            while flag:
                if int((datetime.now() - now).seconds) > 10 or os.path.exists(dirs):
                    flag = False
            with open(dirs, 'w') as f:
                f.write('[settings]\n')
                f.write('default=${project_name}.settings\n')
                f.write('\n')
                f.write('[deploy]\n')
                f.write('url=http://localhost:6800/\n')
                f.write('project=${project_name}\n')
            project_dir = os.path.join('D:\work\scrapyProject', request.form['name'])
            if os.path.exists(project_dir):
                subprocess.Popen(['scrapyd-deploy', '--version', request.form['version']], cwd=project_dir, shell=True)

            project_info = ScrapyProject(name=request.form['name'], spider_count=0, introduce=request.form['introduce'],
                                         create_time=datetime.now(), node_name='', version=request.form['version'])
            opara_log = OperaLog(operation='create_project', person='txl', operation_name=request.form['name'],
                                 create_time=datetime.now())
            db.session.add(opara_log)
            db.session.add(project_info)
            db.session.commit()
        except KeyError as e:
            flash('请填写完整信息..')
        except Exception as e:
            flash('未知错误...')
        return redirect(url_for('spiMain.project_base'))


@scdMain.route('/create_spider', methods=['POST'])
def create_spider():
    # 创建爬虫
    try:
        subprocess.Popen(['scrapy', 'genspider', request.form['name'], request.form['website']],
                         cwd='D:\work\scrapyProject\%s' % request.form['project'])
        spider_info = SpiderInfoDB(name=request.form['name'], sp_url=request.form['website'], run_count=0, item_count=0,
                                   url_count=0, introduce=request.form['introduce'], project=request.form['project'],
                                   create_time=datetime.now(), version='1.0', status='stop')
        # 后面添加读取当前登录用户功能
        opara_log = OperaLog(operation='create_spider', person='txl', operation_name=request.form['name'],
                             create_time=datetime.now())
        db.session.add(spider_info)
        db.session.add(opara_log)
        db.session.commit()
    except KeyError as e:
        _ = e
        flash('请填写完整信息...')
    return redirect(url_for('spiMain.spider_base'))
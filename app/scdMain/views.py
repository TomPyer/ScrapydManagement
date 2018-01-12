#! coding:utf-8
from app.scdMain import scdMain                                 # 自定义app
from flask import render_template, request, redirect, url_for   # 基础内容
from app.models import User, SpiderLog, db                      # 模板内容
from utils.crypt import signature, des_encrypt, gen_md5_salt    # 加密函数
from flask_login import login_required, logout_user             # 路由保护
from app.scdMain.forms import LoginForm, RegisterForm
from flask_mail import Message
from app import mail

import traceback


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
    # 工作页面
    return render_template('work.html')


@scdMain.route('/message', methods=['POST'])
def message():
    # 网页信息发送至开发者邮箱
    msg = Message(request.form['msg_body'], sender='271348762@qq.com', recipients=['zenmeshenmedoubang@qq.com'])
    msg.body = request.form['msg_body']
    mail.send(msg)
    return render_template('contact.html')

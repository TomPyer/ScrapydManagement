#! coding:utf-8
from app.scdMain import scdMain                                 # 自定义app
from flask import render_template, request, redirect, url_for   # 基础内容
from app.models import User, SpiderLog, db                      # 模板内容
from utils.crypt import signature, des_encrypt, gen_md5_salt    # 加密函数
from flask_login import login_required, logout_user             # 路由保护
from .forms import LoginForm, RegisterForm

import traceback


@scdMain.route('/register', methods=['GET', 'POST'])
def register():
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
    return render_template('index.html')


@scdMain.route('/hello', methods=['GET', 'POST'])
@scdMain.route('/', methods=['GET', 'POST'])
@login_required
def hello():
    return render_template('base.html')
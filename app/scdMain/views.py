#! coding:utf-8
from app.scdMain import scdMain                                 # 自定义app
from flask import render_template, request                      # 基础内容
from app.models import User, SpiderLog, db                      # 模板内容
from utils.crypt import signature, des_encrypt, gen_md5_salt    # 加密函数
from flask_login import login_required                          # 路由保护
from .forms import LoginForm


@scdMain.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        token = gen_md5_salt()
        user_obj = User(username=signature(request.args.get('user'), 'tangxl66'),
                        passwd=des_encrypt(request.args.get('passwd'), token), token=token,
                        email=request.args.get('email'), level=request.args.get('level'))
        db.session.add(user_obj)
        db.session.commit()
    return render_template('index.html')


@scdMain.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error, form=form)


def valid_login(user, pwd):
    # 验证账号密码
    username = signature(user, 'tangxl66')
    us_obj = User.query.filter_by(username=bytes(username)).first()
    if us_obj:
        token = us_obj.token
        pwd = des_encrypt(pwd, token)
        if pwd == us_obj.userpwd:
            return render_template('index.html')
        else:
            return render_template('login.html', error='账号或密码错误!')
    else:
        return render_template('login.html', error='账号不存在!')


def log_the_user_in(user):
    pass


@scdMain.route('/he', methods=['GET', 'POST'])
@login_required
def hello_word():
    return render_template('base.html')
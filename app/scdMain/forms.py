#! coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保存密码')
    submit = SubmitField('登陆')


class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(6, 12)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('注册')


class ProjectInfoForm(FlaskForm):
    project_name = StringField('项目名称', validators=[DataRequired()])
    project_spider_num = StringField('爬虫数量', validators=[DataRequired()])
    project_create_date = StringField('项目创建时间', validators=[DataRequired()])
    project_introduce = StringField('项目介绍', validators=[DataRequired()])
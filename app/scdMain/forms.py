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
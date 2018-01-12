#! coding:utf-8

from flask import render_template, request, redirect, url_for, flash
from app.spiMain import spiMain
from flask_login import login_required

from ..scdMain.spiderinfo import SpiderTask, SpiderInfo

from datetime import datetime


@spiMain.route('/cre_task', methods=['POST'])
def cre_task():
    """
    创建爬虫任务
    request.args
        project:    项目名称
        spider:     爬虫名称
        taskType:   调度类型
        year, month, day, hour, minu  年,月,日,时,分
        state:      open/close
    """
    stask_obj = SpiderTask()
    dic_args = {'run_date': datetime(request.form['year'], request.form['month'], request.form['day'],
                                     request.form['hour'], request.form['minu'], 0),
                'start_date': request.form['start_date'],
                'end_date': request.form['end_date'],
                'year': request.form['year'], 'month': request.form['month'],
                'day': request.form['day'], 'hour': request.form['hour'],
                'minute': request.form['minu'], 'days': request.form['day'],
                'hours': request.form['hour'], 'minutes': request.form['minu']
                }
    flag = stask_obj.create_task(request.form['project'], request.form['spider'], request.form['state'],
                                 request.form['taskType'], **dic_args)
    if not flag:
        flash('创建任务失败...请重试')
    return redirect(url_for('scdMain/work'))


@spiMain.route('/start_task', methods=['GET'])
def start_task():
    # 开始任务
    pass


@spiMain.route('/stop_task', methods=['GET'])
def stop_task():
    # 结束任务
    pass


@spiMain.route('/view_task', methods=['GET'])
def view_task():
    # 查看任务
    pass
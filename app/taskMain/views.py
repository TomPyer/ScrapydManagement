#! coding:utf-8

from flask import render_template, request, redirect, url_for, flash
from app.taskMain import taskMain
from flask_login import login_required
from app.models import TaskInfo, OperaLog
from app import db

from datetime import datetime
from utils.SchedUtils import SchedulerUtils
from app.scdMain.spiderinfo import SpiderTask

import uuid


@taskMain.route('/all_task', methods=['GET'])
def all_task():
    # 所有计划任务
    task_info = TaskInfo.query.all()
    re_list = []
    for task in task_info:
        temp_data = {'task_name': task.name, 'work_num': task.work_num, 'create_date': task.create_time,
                     'create_pre': task.create_person, 'status': task.status, 'introduce': task.introduce}
        re_list.append(temp_data)
    return render_template('apsForm/stoped_task.html', re_list=re_list)


@taskMain.route('/effe_task', methods=['GET'])
def effe_task():
    # 有效任务
    task_info = TaskInfo.query.filter_by(status='running').all()
    re_list = []
    for task in task_info:
        temp_data = {'task_name': task.name, 'work_num': task.work_num, 'create_date': task.create_time,
                     'create_pre': task.create_person, 'status': task.status, 'introduce': task.introduce}
        re_list.append(temp_data)
    return render_template('apsForm/stoped_task.html', re_list=re_list)


@taskMain.route('/stoped_task', methods=['GET'])
def stoped_task():
    # 已停止任务
    task_info = TaskInfo.query.filter_by(status='stop').all()
    re_list = []
    for task in task_info:
        temp_data = {'task_name': task.name, 'work_num': task.work_num, 'create_date': task.create_time,
                     'create_pre': task.create_person, 'status': task.status, 'introduce': task.introduce}
        re_list.append(temp_data)
    return render_template('apsForm/stoped_task.html', re_list=re_list)


def myfunc(project, spider):
    from subprocess import Popen
    Popen(['scrapy'], cwd='D:/work/scrapyProject/%s' % project ,shell=True)


@taskMain.route('/create_task', methods=['POST'])
def create_task():
    # 创建任务
    try:
        # sched_obj = SchedulerUtils()
        stask_obj = SpiderTask()
        # id = db.Column(db.Integer, primary_key=True)
        # name = db.Column(db.String(30), index=True)
        # work_num = db.Column(db.Integer)
        # create_time = db.Column(db.DateTime)
        # create_person = db.Column(db.String(50))
        # status = db.Column(db.String(20))
        # introduce = db.Column(db.String(20))
        # 添加创建定时任务流程
        # sched_obj.create_task(myfunc(), task_id=task_id, trigger=request.form['dy_type'], **request.form)
        flag = stask_obj.create_task(request.form['project'], request.form['spider'], 'start', request.form['dy_type'], **request.form)
        if flag:
            task_info = TaskInfo(name=request.form['name'], work_num=0, create_time=datetime.now(),
                                 create_person='tangxl', status='Padding', introduce=request.form['introduce'])
            # 后面添加读取当前登录用户功能
            opara_log = OperaLog(operation='create_task', person='txl', operation_name=request.form['name'],
                                 create_time=datetime.now())
            db.session.add(task_info)
            db.session.add(opara_log)
            db.session.commit()
        else:
            flash('创建任务失败...')
    except KeyError as e:
        _ = e
        flash('请填写完整信息...')
    return redirect(url_for('taskMain.all_task'))
#! coding:utf-8

from flask import render_template, request, redirect, url_for, flash
from app.taskMain import taskMain
from flask_login import login_required

from datetime import datetime


@taskMain.route('/all_task', methods=['GET'])
def all_task():
    # 所有计划任务
    temp_data1 = {'task_name': 'name1', 'work_num': '12', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'tangxl', 'status': 'running'}
    temp_data2 = {'task_name': 'name2', 'work_num': '1', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'ssxx', 'status': 'stop'}
    temp_data3 = {'task_name': 'name3', 'work_num': '5', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'jjjh', 'status': 'stop'}
    temp_data4 = {'task_name': 'name4', 'work_num': '8', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'nnbd', 'status': 'running'}
    re_list = (temp_data1, temp_data2, temp_data3, temp_data4)
    return render_template('apsForm/all_task.html', re_list=re_list)


@taskMain.route('/effe_task', methods=['GET'])
def effe_task():
    # 有效任务
    temp_data1 = {'task_name': 'name1', 'work_num': '12', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'tangxl',
                  'status': 'running'}

    temp_data4 = {'task_name': 'name4', 'work_num': '8', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'nnbd',
                  'status': 'running'}
    re_list = (temp_data1, temp_data4)
    return render_template('apsForm/effe_task.html', re_list=re_list)


@taskMain.route('/stoped_task', methods=['GET'])
def stoped_task():
    # 已停止任务
    temp_data2 = {'task_name': 'name2', 'work_num': '1', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'ssxx',
                  'status': 'stop'}
    temp_data3 = {'task_name': 'name3', 'work_num': '5', 'create_date': '2018年1月18日 11:39:21', 'create_pre': 'jjjh',
                  'status': 'stop'}
    re_list = (temp_data2, temp_data3)
    return render_template('apsForm/stoped_task.html', re_list=re_list)


@taskMain.route('/create_task', methods=['POST'])
def create_task():
    # 创建任务
    return redirect(url_for('taskMain.all_task'))
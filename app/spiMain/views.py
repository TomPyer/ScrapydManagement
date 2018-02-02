#! coding:utf-8

import os
import datetime
from lxml import etree

from flask import render_template, request, redirect, url_for, flash, current_app
from app.spiMain import spiMain
from flask_login import login_required, current_user
from app import db

from ..scdMain.spiderinfo import SpiderTask, SpiderInfo
from app.models import ScrapyProject, SpiderInfoDB


@spiMain.route('/action_spider', methods=['POST'])
@login_required
def action_spider():
    # 开始爬虫
    stask_obj = SpiderTask()
    spider_obj = SpiderInfoDB()
    flag = ret = ''
    if request.form['act'] == 'stop':
        # 数据库状态为stop则触发启动功能
        flag, ret = stask_obj.start_spider(request.form['project'], request.form['spider'])
        db_obj = spider_obj.query.filter_by(name=request.form['spider'], project=request.form['project']).all()
        db_obj[0].status = 'running'
        db.session.commit()
    elif request.form['act'] == 'running':
        flag = stask_obj.stop_spider(request.form['project'], request.form['spider'])
        db_obj = spider_obj.query.filter_by(name=request.form['spider'], project=request.form['project']).all()
        db_obj[0].status = 'stop'
        db.session.commit()
    else:
        flash('错误的请求方式')
    if not flag:
        flash(ret)
    return redirect(url_for('spiMain.spider_base'))


@spiMain.route('/view_spider', methods=['POST'])
@login_required
def view_task():
    # 查看爬虫
    spider_obj = SpiderInfo()
    run_info = spider_obj.get_spider_info(request.args.get('project'), request.args.get('spider_run_id'))
    return render_template('work.html', runInfo=run_info)


@spiMain.route('/project_base', methods=['GET'])
@login_required
def project_base():
    # 项目页面
    project_info = ScrapyProject.query.all()
    re_list = []
    for project in project_info:
        temp_data = {'project_name': project.name, 'spiders': project.spider_count, 'node_name': project.node_name,
                     'create_date': project.create_time, 'version': project.version, 'introduce': project.introduce}
        re_list.append(temp_data)
    return render_template('apsForm/project_base.html', re_list=re_list, user=current_user.username, email=current_user.email,
                           level=current_user.level, counts=current_user.project_count, typ='项目')


@spiMain.route('/spider_base', methods=['GET', 'POST'])
@login_required
def spider_base():
    # 爬虫页面
    spider_info = SpiderInfoDB.query.all()
    project_info = ScrapyProject.query.all()
    re_list = []
    project_list = []
    if request.args.get('project'):
        spider_info = SpiderInfoDB.query.filter_by(project=request.args.get('project')).all()
    for spider in spider_info:
        temp_data = {'spider': spider.name, 'project': spider.project, 'node_name': '', 'create_date': spider.create_time,
                   'version': spider.version, 'status': spider.status, 'status_time(minu)': spider.run_time, 'spider_url': spider.sp_url}
        re_list.append(temp_data)
    for p in project_info:
        project_list.append(p.name)
    return render_template('apsForm/spider_base.html', re_list=re_list, project_list=project_list, user=current_user.username, email=current_user.email,
                           level=current_user.level, counts=current_user.spider_count, typ='爬虫')


@spiMain.route('/spider_run_base', methods=['GET'])
@login_required
def spider_run_base():
    # 运行中爬虫页面
    spider_info = SpiderInfoDB.query.filter_by(status='running').all()
    project_info = ScrapyProject.query.all()
    re_list = []
    project_list = []
    for spider in spider_info:
        temp_data = {'spider': spider.name, 'project': spider.project, 'node_name': '',
                     'create_date': spider.create_time,
                     'version': spider.version, 'status': spider.status, 'status_time(minu)': spider.run_time}
        re_list.append(temp_data)
    for p in project_info:
        project_list.append(p.name)
    return render_template('apsForm/spider_base.html', re_list=re_list, project_list=project_list, user=current_user.username, email=current_user.email,
                           level=current_user.level, counts=current_user.spider_count, typ='爬虫')


@spiMain.route('/spider_pad_base', methods=['GET'])
@login_required
def spider_pad_base():
    # 待运行爬虫页面
    spider_info = SpiderInfoDB.query.filter_by(status='padding').all()
    project_info = ScrapyProject.query.all()
    re_list = []
    project_list = []
    for spider in spider_info:
        temp_data = {'spider': spider.name, 'project': spider.project, 'node_name': '',
                     'create_date': spider.create_time,
                     'version': spider.version, 'status': spider.status, 'status_time(minu)': spider.run_time}
        re_list.append(temp_data)
    for p in project_info:
        project_list.append(p.name)
    return render_template('apsForm/spider_base.html', re_list=re_list, project_list=project_list, user=current_user.username, email=current_user.email,
                           level=current_user.level, counts=current_user.spider_count, typ='爬虫')


@spiMain.route('/suc_task', methods=['GET'])
@login_required
def suc_task():
    # 已完成任务页面
    spiinfo_obj = SpiderInfo()
    re_list = []
    project_dic = spiinfo_obj.get_scrapy_project_info()
    for k, _ in project_dic.items():
        work_info = spiinfo_obj.get_jbos_info(k)
        # for task in work_info['pending']:
        #     if task:
        #         run_time = datetime.strptime(task['start_time'].split('.')[0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(
        #             task['end_time'].split('.')[0], "%Y-%m-%d %H:%M:%S")
        #         re_list.append({'project': k, 'spider': task['spider'], 'job': task['id'], 'start': task['start_time'],
        #                         'runtime': (86400 - int(run_time.seconds)), 'finish': task['end_time'], 'status': 'pending',
        #                         'log': ''.join([current_app.confit['SCRAPYD_URL'],
        #                                         '/logs/%s/%s/%s.log' % (k, task['spider'], task['id'])])})
        # for task in work_info['running']:
        #     if task:
        #         run_time = datetime.strptime(task['start_time'].split('.')[0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(
        #             task['end_time'].split('.')[0], "%Y-%m-%d %H:%M:%S")
        #         re_list.append({'project': k, 'spider': task['spider'], 'job': task['id'], 'start': task['start_time'],
        #                         'runtime': (86400 - int(run_time.seconds)), 'finish': task['end_time'], 'status': 'running',
        #                         'log': ''.join([current_app.confit['SCRAPYD_URL'],
        #                                         '/logs/%s/%s/%s.log' % (k, task['spider'], task['id'])])})
        for task in work_info['finished']:
            if task:
                run_time = datetime.datetime.strptime(task['start_time'].split('.')[0], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(task['end_time'].split('.')[0], "%Y-%m-%d %H:%M:%S")
                re_list.append({'project': k, 'spider': task['spider'], 'job': task['id'], 'start': task['start_time'].split('.')[0],
                                'runtime': (86400 - int(run_time.seconds)), 'finish': task['end_time'].split('.')[0], 'status': 'finished',
                                'log': ''.join([current_app.config['SCRAPYD_URL'], 'logs/%s/%s/%s.log' % (k, task['spider'], task['id'])])})

    return render_template('apsForm/suc_task.html', re_list=re_list, user=current_user.username, email=current_user.email,
                           level=current_user.level, counts=current_user.task_count, typ='任务')


@spiMain.route('/write_spider', methods=['GET'])
def selector():
    # 解析页面
    file_body = None
    return render_template('apsForm/file_page.html', file_body=file_body)


@spiMain.route('/get_rules', methods=['GET', 'POST'])
def get_rules():
    from flask import jsonify
    re_list = []
    for i in range(6):
        temp_data = {'allowed_domains': 'www.baidu.com', 'start_url': 'www.baidu.com',
                     'next_page': '//div[@class="questionsList"]', 'body1': '//div[@class="asdas123"]',
                     'body2': '//div[@class="12lll"]',
                     'body3': '//table[class="lkppo"]'}
        re_list.append(temp_data)
    return jsonify(re_list)


@spiMain.route('/modify_rules', methods=['POST'])
def modify_rules():
    pass
#! coding:utf-8

import urllib.request
import urllib.parse

from flask import current_app               # 配置项获取
from utils.urllibfunc import get_url_act, post_url_act      # 获取request相关方法


class SpiderInfo(object):
    """
    爬虫相关信息获取类
    """

    def __init__(self):
        self.spiders_count = 0
        self.projects_count = 0
        self.running_count = 0
        self.stop_count = 0
        self.pending = 0

    def get_spider_info(self, project_name, spider_id):
        # 获取爬虫信息
        jobs_info = self.get_jbos_info(project_name)
        for spider in jobs_info:
            if spider['id'] == spider_id:
                return spider

    def get_jbos_info(self, project_name):
        # 获取工程信息, 项目下所有的爬虫作业信息
        url = '?'.join([current_app.config['GET_PROJECT_JOBS_INFO'], 'project=', project_name])
        resp = get_url_act(url)
        rfp_lis = resp['running'] + resp['finished'] + resp['pending']      # 三种状态的爬虫信息
        self.running_count = len(resp['running'])
        self.stop_count = len(resp['finished'])
        self.pending = len(resp['finished'])
        return rfp_lis

    def get_scrapy_project_info(self):
        # 获取项目信息
        response = get_url_act(current_app.config['GET_PROJECTS_URL'])
        project_list = response['projects']
        project_dic = {}
        self.projects_count = len(project_list)
        for project_name in project_list:
            resp = post_url_act(current_app.config['GET_SPIDERS_URL'], data={'project': project_name})
            project_dic[project_name] = resp['spiders']
            self.spiders_count += len(resp['spiders'])
        return project_dic


class SpiderTask(object):
    """
    爬虫工作相关,新建任务,关闭任务
    """
    def __init__(self):
        pass

    @staticmethod
    def start_spider(project_name, spider_name):
        # 开始任务
        resp = post_url_act(url=current_app.config['START_SPIDER_URL'],
                            data={'project': project_name, 'spider': spider_name})
        return resp

    @staticmethod
    def stop_spider(project_name, spider_id):
        # 结束任务
        resp = post_url_act(url=current_app.config['STOP_SPIDER_URL'],
                            data={'project': project_name, 'spider': spider_id})
        return resp

    @staticmethod
    def create_task(project_name, spider):
        # 创建任务(定时启动或关闭)
        pass
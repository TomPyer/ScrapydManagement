#! coding:utf-8
"""
任务调度工具
"""

from apscheduler.schedulers.background import BackgroundScheduler
# 当没有运行任何其他框架并希望调度器在你应用的后台执行时使用
from apscheduler.jobstores.redis import RedisJobStore       # 用redis作backend
from apscheduler.jobstores.memory import MemoryJobStore     # 默认的内存backend
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor  # 线程池和进程池

from flask import current_app

from datetime import datetime


class SchedulerUtils(object):
    """
    任务调度工具
    """
    def __init__(self):
        self.sched = self.create_scheduler()

    @staticmethod
    def create_scheduler():
        # 创建Scheduler对象
        # redis_pool = redis.Connection(host=current_app['REDIS_HOST'], port=current_app.config['REDIS_PORT'])
        # redis_pool = redis.Connection(host='127.0.0.1', port='6379')
        jobstores = {
            'redis': RedisJobStore(),  # redis作为调度仓库
            'default': MemoryJobStore()  # 默认的内存作为调度仓库
        }
        executors = {
            'default': ThreadPoolExecutor(200),  # 进程池
            'processpool': ProcessPoolExecutor(10)  # 线程池
        }
        job_defaults = {
            'coalesce': True,  # 因系统原因任务被挂起,导致任务存在多个,恢复正常后是否多次执行
            'max_instances': 1,  # 同个job同一时间最多存在几个实例在运行(上一次任务未执行完毕的话后续任务则不执行)
            'misfire_grace_time': 60  # 某个job因其他原因导致未在时间点上执行,超过多少分钟后则不执行
        }
        sched = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        return sched

    def create_task(self, func, task_id, trigger, jobstore='redis', **kwargs):
        """
        创建新任务
        :param func:    需要执行的具体函数
        :param task_id: 该次任务的ID
        :param trigger: 调度策略
        :param jobstore:任务存储器
        :param kwargs:    具体执行的时间(根据不同调度策略有不同的值)
        :return:        None
        """
        task_id = str(task_id)
        if trigger == 'cron':
            # 暂不启用
            self.sched.add_job(func, trigger, jobstore=jobstore, id=task_id, start_date=self.date_zh(kwargs['start_time']),
                               end_date=self.date_zh(kwargs['end_time']), year=kwargs['year'], month=kwargs['month'],
                               day=kwargs['day'], hour=kwargs['hour'], minute=kwargs['minute'], second=0,
                               replace_existing=True)
        elif trigger == 'date':
            self.sched.add_job(func, trigger, jobstore=jobstore, id=task_id, run_date=self.date_zh(kwargs['start_time']),
                               replace_existing=True)
        elif trigger == 'interval':
            #  days=kwargs['days'], hours=kwargs['hours'], minutes=kwargs['minutes'], seconds=kwargs['seconds'],
            if kwargs['dy_value'] == 'd':
                self.sched.add_job(func, trigger, jobstore=jobstore, id=task_id, days=kwargs['dy_vv'],
                                   start_date=self.date_zh(kwargs['start_time']),
                                   end_date=self.date_zh(kwargs['end_time']))
            elif kwargs['dy_value'] == 'h':
                self.sched.add_job(func, trigger, jobstore=jobstore, id=task_id, hours=kwargs['dy_vv'],
                                   start_date=self.date_zh(kwargs['start_time']),
                                   end_date=self.date_zh(kwargs['end_time']))
            elif kwargs['dy_value'] == 'm':
                self.sched.add_job(func, trigger, jobstore=jobstore, id=task_id, minutes=kwargs['dy_vv'],
                                   start_date=self.date_zh(kwargs['start_time']),
                                   end_date=self.date_zh(kwargs['end_time']))
            elif kwargs['dy_value'] == 's':
                self.sched.add_job(func, trigger, jobstore=jobstore, id=task_id, seconds=kwargs['dy_vv'],
                                   start_date=self.date_zh(kwargs['start_time']),
                                   end_date=self.date_zh(kwargs['end_time']))
        self.sched.start()

    def remove_task(self, task_id, jobstore='redis'):
        # 删除任务
        self.sched.remove_job(task_id, jobstore=jobstore)

    def modify_task(self, task_id, date_dic, trigger='cron', ):
        """
        修改任务
        :param task_id:  任务id
        :param trigger:  修改后的触发类型
        :param date_dic: 定时参数
        :return:         None
        """
        self.sched.reschedule_job(task_id, trigger=trigger, start_data=date_dic['start_date'],
                                  end_date=date_dic['end_date'], )

    def close_sched(self, wait):
        """
        关闭调度器
        :param wait:    是否等待所有作业完成, 默认为True
        :return:        None
        """
        self.sched.shutdown(wait=wait)

    def get_tasks(self):
        return self.sched.get_jobs()

    def date_zh(self, dates):
        # ['2018年1月23日 17:11:34']
        year = int(dates[0].split('年')[0])
        month = int(dates[0].split('月')[0].split('年')[1])
        day = int(dates[0].split('月')[1].split('日')[0])
        other = dates[0].split(' ')[1].split(':')
        return datetime(year, month, day, int(other[0]), int(other[1]), int(other[2]))

    """ cron 定时调度 (某一定时刻执行)
        ----(int|str) 表示参数既可以是int类型，也可以是str类型
        ----(datetime | str) 表示参数既可以是datetime类型，也可以是str类型
        year (int|str) – 4-digit year -（表示四位数的年份，如2008年）
        month (int|str) – month (1-12) -（表示取值范围为1-12月）
        day (int|str) – day of the (1-31) -（表示取值范围为1-31日）
        week (int|str) – ISO week (1-53) -（格里历2006年12月31日可以写成2006年-W52-7（扩展形式）或2006W527（紧凑形式））
        day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun) - （表示一周中的第几天，既可以用0-6表示也可以用其英语缩写表示）
        hour (int|str) – hour (0-23) - （表示取值范围为0-23时）
        minute (int|str) – minute (0-59) - （表示取值范围为0-59分）
        second (int|str) – second (0-59) - （表示取值范围为0-59秒）
        start_date (datetime|str) – earliest possible date/time to trigger on (inclusive) - （表示开始时间）
        end_date (datetime|str) – latest possible date/time to trigger on (inclusive) - （表示结束时间）
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone) -（表示时区取值）
        ---表示2017年3月22日17时19分07秒执行该程序
        scheduler.add_job(my_job, 'cron', year=2017,month = 03,day = 22,hour = 17,minute = 19,second = 07)
    """

    """ interval 间隔调度  （任务会多次执行）
        weeks (int) – 某周
        days (int) – 某日
        hours (int) – 某时
        minutes (int) – 某分钟
        seconds (int) – number of seconds to wait   某秒
        start_date (datetime|str) – starting point for the interval calculation   任务起始时间
        end_date (datetime|str) – latest possible date/time to trigger on   任务结束时间
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations 时区
        ---表示每隔3天17时19分07秒执行一次任务
        scheduler.add_job(my_job, 'interval', days=03, hours=17, minutes=19, seconds=07)
    """

    """ date 定时调度   (仅执行一次)
        run_date (datetime|str) – the date/time to run the job at  -任务开始的时间
        timezone (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already
        ---在指定的时间，只执行一次
        scheduler.add_job(tick, 'date', run_date='2018年1月11日 17:02:14')　
    """


def testfunc():
    return 'lalalalalla'

if __name__ == "__main__":
    sch_obj = SchedulerUtils()
    sch_obj.create_task(testfunc, 'test2', 'interval')
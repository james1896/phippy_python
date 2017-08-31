# -*- coding: utf-8 -*-
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import json

from . import common

@common.route('/')
def app_index():
    return 'hello common'



###########################################################################
############### 定时任务 两小时一次获得当前天气 ###############################

#######################################################
#                                                     #
#                   参考网址                           #
#   python调度框架APScheduler使用详解                   #
#   http://www.cnblogs.com/hushaojun/p/5189109.html   #
#                                                     #
#######################################################
#
#               api 接口
#       https://www.apixu.com/my/
#
#######################################################



# Partly cloudy         局部多云
# Light rain shower     小阵雨

weater_last_update_time = ''
weather_temp_c          = ''
weather_condition_text  = ''
weather_condition_icon  = ''


def my_job():
    print time.strftime('请求时间: %Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:

        import urllib, urllib2
        req = urllib2.Request(url='http://api.apixu.com/v1/current.json?key=36aebc1dd360486b98382012173008&q=Makati')
        res = urllib2.urlopen(req)
        res = res.read()

        current_dict = json.loads(res)
        current_dict = current_dict['current']
        weater_last_update_time = current_dict['last_updated']
        weather_temp_c          = current_dict['temp_c']
        condition_dict = current_dict['condition']
        weather_condition_text = condition_dict['text']

        print(weater_last_update_time, weather_temp_c,weather_condition_text)
    except Exception,e:
        print e

scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'interval', hours=2)
scheduler.start()    #这里的调度任务是独立的一个线程
# sched = BlockingScheduler()
# sched.add_job(my_job, 'interval', hours=2)
# sched.start()

################################### 定时任务 两小时一次获得当前天气 ###############################
###############################################################################################
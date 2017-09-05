# -*- coding: utf-8 -*-
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import json

from . import common

@common.route('/')
def app_index():
    return 'hello common'

#版本号比较
import re
def versionCompare(v1="1.1.1", v2="1.2"):
    v1_check = re.match("\d+(\.\d+){0,2}", v1)
    v2_check = re.match("\d+(\.\d+){0,2}", v2)
    if v1_check is None or v2_check is None or v1_check.group() != v1 or v2_check.group() != v2:
        return "版本号格式不对，正确的应该是x.x.x,只能有3段"
    v1_list = v1.split(".")
    v2_list = v2.split(".")
    v1_len = len(v1_list)
    v2_len = len(v2_list)
    if v1_len > v2_len:
        for i in range(v1_len - v2_len):
            v2_list.append("0")
    elif v2_len > v1_len:
        for i in range(v2_len - v1_len):
            v1_list.append("0")
    else:
        pass
    for i in range(len(v1_list)):
        if int(v1_list[i]) > int(v2_list[i]):
            return 1
        if int(v1_list[i]) < int(v2_list[i]):
            return -1
    return 0

# 测试用例
# print(versionCompare(v1="", v2=""))
# print(versionCompare(v1="1.0.a", v2="d.0.1"))
# print(versionCompare(v1="1.0.1", v2="1.0.1"))
# print(versionCompare(v1="1.0.2", v2="1.0.1"))
# print(versionCompare(v1="1.4.1", v2="2.1.2"))
# print(versionCompare(v1="1.0.11", v2="1.0.2"))

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
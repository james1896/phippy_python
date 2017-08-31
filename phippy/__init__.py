# -*- coding: utf-8 -*-
import os

import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import request, json
from flask import Flask, render_template, jsonify

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from phippy.config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

# rsa解密
# def decryption(encode_value):
#     return rsaCipher.decryptionWithString(encode_value, random_generator)
# # 解密成string
# decodeStr = decryption(value)
# # jsonn --> dictt
# value_dict = json.loads(decodeStr)

#加载配置文件内容
app.config.from_object('phippy.config')     #模块下的setting文件名，不用加py后缀



# 创建实例，并连接test库
# echo=True 显示信息
engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       encoding="utf-8",
                       echo=False)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# 生成orm基类
Base = declarative_base()
Base.query = db_session.query_property()


# 注册蓝图
from users.user import user as user_blurprint
from merchant.merchant import merchant as merchant_blurprint
from common.common import common as common_blurprint

app.register_blueprint(user_blurprint, url_prefix='/user')
app.register_blueprint(merchant_blurprint, url_prefix='/merchant')
app.register_blueprint(common_blurprint, url_prefix='/common')

###############################################################################################
################################### 定时任务 两小时一次获得当前天气 ###############################

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



# Partly cloudy  局部多云

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

@app.route('/')
def hello_world():
    init_db()

    return render_template("app_download.html")
    # return render_template("phone_type.html")


@app.route('/forapp',methods=['GET','POST'])

# app初始化的时候调用

def forapp():

    return jsonify({"a":"b"})


###########################################################################################
###########################################################################################
###########################################################################################



###############################################################
###############################################################




def init_db():
    Base.metadata.create_all(bind=engine)


# if __name__ == '__main__':
#     app.run('10.71.66.2', debug=True, port=5001)


# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
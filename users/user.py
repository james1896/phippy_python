# -*- coding: utf-8 -*-

# 得到商家（根据store_type区分是旅行社还是餐馆）
from  datetime  import  *

from flask import request, jsonify

from phippy import db_session
from phippy.model.userBehaviour import Userbehaviour
from phippy.model.article import Article
from phippy.model.goods import Goods
from phippy.model.order import Order
from phippy.model.store import Store
from phippy.model.venv import Venv
from users import code
from . import user
from code import statusCode

@user.route('/')
def app_index():
    return "hello user"

#version , platform(ios_phippy,android_phippy)

@user.route('/initializeUser', methods=['GET', 'POST'])
def initializeUser():

    if request.method != 'POST':
        return jsonify({statusCode:code.isNotPost})

    ip      = request.form.get('ip')
    userid  = request.form.get('userid')
    time    = request.form.get('time')
    uuid    = request.form.get('uuid')
    device  = request.form.get('device')
    version = request.form.get('version')
    language = request.form.get('language')
    platform = ''

    print ip
    print userid
    print time
    print uuid
    print device
    print version
    print language
    print "------------"

    strs = device.split('|')

    # 字符串拆分不符合规则
    if len(strs) != 2:
        return jsonify({statusCode:code.internalError})

    latestVersion = ''

    # 查询当前最新版本号
    venv = Venv()
    try:
        venv = Venv.query.filter().first()
    except Exception,e:
        return jsonify({statusCode: code.sql_error})
        print e

    if 'ios' in strs[0].lower():
        platform = 'ios'
        device = strs[1]
        latestVersion = venv.ios_version_user
    if 'android' in strs[0].lower():
        platform = 'android'
        device = strs[1]
        latestVersion = venv.android_version_user

    from common.common import versionCompare
    isupdate = versionCompare(latestVersion,version)
    if isupdate == 0:
        print "当前app是最新版本"

    elif isupdate == 1:
        print "有新版本，请更新"

    elif isupdate == -1:
        # 有错误不暴漏
        isupdate = -1
        print '有错误'
        return jsonify({statusCode: code.internalError})
    else:
        print '参数错误'
        return jsonify({statusCode: code.internalError})

    # 收集用户信息入库
    if isupdate == 0 or isupdate == 1:

        behaviour           = Userbehaviour()
        behaviour.ip        = ip
        behaviour.username  = userid
        behaviour.time      = datetime.today()
        behaviour.uuid      = uuid
        behaviour.device    = device
        behaviour.version   = version
        behaviour.language  = language
        behaviour.platform  = platform
        try:
            db_session.add(behaviour)
            db_session.commit()
        except Exception,e:
            return jsonify({statusCode: code.sql_error})
            print e

    return jsonify({statusCode:code.success,
                    code.isUpdate:isupdate})


# from users import views
# 得到商家（根据store_type区分是旅行社还是餐馆）
@user.route('/getstore', methods=['GET', 'POST'])
def findStore():
    if request.method != 'POST':
        return jsonify({statusCode:code.isNotPost})

    store_type = request.form.get('store_type')
    stores = Store.query.filter(Store.store_type == store_type).all()
    list = []
    for store in stores:
        dict = {}
        dict['adress'] = store.adress
        dict['name'] = store.name
        dict['rank'] = store.rank
        dict['wechat'] = store.wechat
        dict['img_url'] = store.img_url
        dict['store_id'] = store.store_id
        dict['store_type'] = store.store_type
        dict['deliver_time'] = store.deliver_time
        dict['phone_number'] = store.phone_number
        dict['qisong_condition'] = store.qisong_condition

        list.append(dict)

    return jsonify({statusCode: code.success, 'data': list})


# 得到旅行相关的文章
@user.route('/getarticle', methods=['GET', 'POST'])
def getarticle():
    if request.method != 'POST':
        return jsonify({statusCode:code.isNotPost})

    articles = Article.query.filter().all()
    list = []
    for article in articles:
        dict = {}
        dict['store_id'] = article.store_id
        dict['title'] = article.title
        dict['content'] = article.content
        dict['time'] = article.time
        dict['img_url'] = article.img_url
        dict['rank'] = article.rank

        list.append(dict)
    return jsonify({statusCode: code.success, 'data': list})


# 得到餐品
@user.route('/getgoods', methods=['POST'])
def getfood():
    if request.method != 'POST':
        return jsonify({statusCode:code.isNotPost})

    try:
        store_id = request.form.get('store_id')
        goods = Goods.query.filter(Goods.store_id == store_id).all()
        list = []
        for tmp in goods:
            dict = {}
            dict['goods_id'] = tmp.goods_id
            dict['store_id'] = tmp.store_id
            dict['name'] = tmp.name
            dict['price'] = tmp.price
            dict['rank'] = tmp.rank
            dict['img_url'] = tmp.img_url
            dict['publish_time'] = tmp.publish_time
            dict['publisher'] = tmp.publisher
            dict['remark'] = tmp.remark
            dict['describe'] = tmp.describe

            list.append(dict)

        return jsonify({statusCode: code.success, 'data': list})
    except Exception,e:
        print e
        return jsonify({statusCode:code.sql_error})


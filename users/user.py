# -*- coding: utf-8 -*-

# 得到商家（根据store_type区分是旅行社还是餐馆）
from flask import request, jsonify
from phippy.model.article import Article
from phippy.model.goods import Goods
from phippy.model.order import Order
from phippy.model.store import Store
from phippy.model.venv import Venv
from . import user

@user.route('/')
def app_index():
    return "hello user"

@user.route('/initializeUser', methods=['GET', 'POST'])
def initializeUser():
    if request.method != 'POST':
        return jsonify({"msg": "is error"})

    # version = Venv.query.filter(Venv.version_user == store_type).all()
    return jsonify({'code':'100'})


# from users import views
# 得到商家（根据store_type区分是旅行社还是餐馆）
@user.route('/getstore', methods=['GET', 'POST'])
def findStore():
    # if request.method != 'POST':
    #     return jsonify({"msg": "is not post"})

    store_type = request.form.get('store_type')
    stores = Store.query.filter(Store.store_type == store_type).all()
    order = Order.query.filter().all()
    list = []
    for store in stores:
        dict = {}
        dict['store_id'] = store.store_id
        dict['store_type'] = store.store_type
        dict['name'] = store.name
        dict['img_url'] = store.img_url
        dict['phone_number'] = store.phone_number
        dict['wechat'] = store.wechat
        dict['deliver_time'] = store.deliver_time
        dict['qisong_condition'] = store.qisong_condition

        dict['adress'] = store.adress
        dict['rank'] = store.rank

        list.append(dict)
    return jsonify({"interface": "得到商家", 'data': list})


# 得到旅行相关的文章
@user.route('/getarticle', methods=['GET', 'POST'])
def getarticle():
    if request.method != 'POST':
        return jsonify({"msg": "is error"})

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
    return jsonify({"interface": "得到旅行相关的文章", 'data': list})


# 得到餐品
@user.route('/getgoods', methods=['POST'])
def getfood():
    if request.method != 'POST':
        return jsonify({"msg": "is error"})

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

    return jsonify({"interface": "得到餐品", 'data': list})
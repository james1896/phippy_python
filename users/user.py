# -*- coding: utf-8 -*-

# 得到商家（根据store_type区分是旅行社还是餐馆）
from flask import request, jsonify

from phippy_python import Store
from users import user

@user.route('/')
def index():
    return "hello user"

@user.route('/getstore',methods=['GET','POST'])
def findStore():

    if request.method != 'POST':
        return jsonify({"msg":"is not post"})

    store_type = request.form.get('store_type')
    stores = Store.query.filter(Store.store_type == store_type).all()
    list = []
    for store in stores:
        dict = {}
        dict['store_id']        = store.store_id
        dict['store_type']      = store.store_type
        dict['name']            = store.name
        dict['img_url']         = store.img_url
        dict['phone_number']    = store.phone_number
        dict['wechat']          = store.wechat
        dict['deliver_time']    = store.deliver_time
        dict['qisong_condition'] = store.qisong_condition

        dict['adress']          = store.adress
        dict['rank']            = store.rank

        list.append(dict)
    return jsonify({"interface":"得到商家",'data':list})
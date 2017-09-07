# -*- coding: utf-8 -*-
import os

from flask import request, jsonify, send_from_directory, Response
from sqlalchemy import desc

from werkzeug.utils import secure_filename

from phippy import db_session
from phippy.model.store import Store
from phippy.model.goods import Goods
from users import code
from users.code import statusCode

from . import merchant


@merchant.route('/')
def app_index():
    return 'hello merchant'

# 待测试
@merchant.route('/addgoods', methods=['GET', 'POST'])
def addgoods():
    store_id = request.form.get('store_id')
    name = request.form.get('name')
    price = request.form.get('price')
    publish_time = request.form.get('publish_time')
    publisher = request.form.get('publisher')

    stores = Store.query.filter(Store.store_id == store_id).all()

    # 判断 store_id 是否正确
    if (len(stores) != 1):
        return jsonify({statusCode: code.addgoods_not_find_storeid})

    # 降序排列
    goods = Goods.query.order_by(desc(Goods.goods_id)).limit(1)

    if goods:

        # 插入数据
        add_goods_id = goods.goods_id + 1
        goods =  Goods()
        goods.store_id = store_id
        goods.goods_id = add_goods_id
        goods.name = name
        goods.price = price
        goods.publish_time = publish_time
        goods.publisher = publisher
        try:
            db_session.add(goods)
            db_session.commit()

        # 如果数据插入成功，上传图片
            addGoodsImg(imgName=name)
            return goods
        except Exception, e:
            # print "用户名 重复", e
            return None


    else:
        return jsonify({'errror': '1'})

def addGoodsImg(imgName):

    store_id = request.form.get('store_id')
    stores = Store.query.filter(Store.store_id == store_id).all()

    # 判断 store_id 是否正确
    if (len(stores) != 1):
        return jsonify({'error': '错误'})


        # file = request.files['file']
        # 表示，从request请求的files字典中，
        # 取出file对应的文件。这个文件是一个FileStorage对象

        # request的files属性，files是一个MultiDict的形式，
        # 而里面的每个文件，都是一个FileStorage对象
    file = request.files['file']
    if file and allowed_file(file.filename):
        # 再来看下这个函数的功能，其实他为了保证文件名不会影响到系统，
        # 他就把文件名里面的斜杠和空格，替换成了下划线
        # 这样，就保证了文件只会在当前目录使用，而不会由于路径问题被利用去做其他事情。
        # 所以，在储存文件之前，通过这个函数把文件名先修改一下



        # 当前文件所在路径
        filename = secure_filename(file.filename)

        # 这个文件对象拥有一个函数功能来保存文件，叫做save()
        # 这个文件对象还拥有一个属性来提取文件名，叫做filename
        # file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        basepath = os.path.dirname(__file__)

        # 判断store分类的文件夹是否存在
        store_dir_path = os.path.join(basepath, UPLOAD_FOLDER, 'store')
        if not os.path.exists(store_dir_path):
               os.makedirs(store_dir_path)

        # 判断当前商家的图片文件夹是否存在
        save_image_path = os.path.join(basepath, UPLOAD_FOLDER, store_id)
        if not os.path.exists(save_image_path):
            print 'ss'
            os.makedirs(save_image_path)

        # 保存图片
        file.save(os.path.join(save_image_path, imgName+'.png'))

        # --------------------------------------------------------------------------
        # 获取文件和文件夹大小 (tyte)
        # --------------------------------------------------------------------------
        # import os
        # from os.path import join, getsize
        # os.path.getsize  获取文件大小 (bytes)


        # def getdirsize(dir):
        #     size = 0L
        #     for root, dirs, files in os.walk(dir):
        #         size += sum([getsize(join(root, name)) for name in files])
        #     return size
        # --------------------------------------------------------------------------
        return jsonify({'a': 'b'})
    return jsonify({'error': '1'})



############################    服务器 image     #############################################
############################    服务器 image     #############################################
############################    服务器 image     #############################################

##上传图片到服务器

#####需要请教大神#########
# 上传文件到服务器，可能存在安全隐患

# 上传图片到根目录下载images文件夹
UPLOAD_FOLDER = r'images'

# 添加指定允许文件类型的范围
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# 判断上传文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@merchant.route('/img', methods=['POST'])
def getimg():
    store_id = request.form.get('store_id')
    stores = Store.query.filter(Store.store_id == store_id).all()

    # 判断 store_id 是否正确
    if (len(stores) != 1):
        return jsonify({'error': '错误'})


        # file = request.files['file']
        # 表示，从request请求的files字典中，
        # 取出file对应的文件。这个文件是一个FileStorage对象

        # request的files属性，files是一个MultiDict的形式，
        # 而里面的每个文件，都是一个FileStorage对象
    file = request.files['file']
    if file and allowed_file(file.filename):
        # 再来看下这个函数的功能，其实他为了保证文件名不会影响到系统，
        # 他就把文件名里面的斜杠和空格，替换成了下划线
        # 这样，就保证了文件只会在当前目录使用，而不会由于路径问题被利用去做其他事情。
        # 所以，在储存文件之前，通过这个函数把文件名先修改一下



        # 当前文件所在路径
        filename = secure_filename(file.filename)

        # 这个文件对象拥有一个函数功能来保存文件，叫做save()
        # 这个文件对象还拥有一个属性来提取文件名，叫做filename
        # file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        basepath = os.path.dirname(__file__)

        # 判断store分类的文件夹是否存在
        store_dir_path = os.path.join(basepath, UPLOAD_FOLDER, 'store')
        if not os.path.exists(store_dir_path):
            os.makedirs(store_dir_path)

        # 判断当前商家的图片文件夹是否存在
        save_image_path = os.path.join(basepath, UPLOAD_FOLDER, store_id)
        if not os.path.exists(save_image_path):
            print 'ss'
            os.makedirs(save_image_path)

        # 保存图片
        file.save(os.path.join(save_image_path, 'fileName.png'))

        # --------------------------------------------------------------------------
        # 获取文件和文件夹大小 (tyte)
        # --------------------------------------------------------------------------
        # import os
        # from os.path import join, getsize
        # os.path.getsize  获取文件大小 (bytes)


        # def getdirsize(dir):
        #     size = 0L
        #     for root, dirs, files in os.walk(dir):
        #         size += sum([getsize(join(root, name)) for name in files])
        #     return size
        # --------------------------------------------------------------------------
        return jsonify({'a': 'b'})
    return jsonify({'error': '1'})


@merchant.route('/imgs', methods=['POST'])
def getimgs():
    files = request.files.getlist('files')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 当前文件所在路径
            basepath = os.path.dirname(__file__)
            print os.path.join(basepath, UPLOAD_FOLDER, filename)
            file.save(os.path.join(basepath, UPLOAD_FOLDER, filename))
        else:
            print 'budui'

    return jsonify({'error': '1'})


# 通过图片名 得到某个图片
@merchant.route('/uploadedfile/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


##下载服务器图片
@merchant.route('/image/<imageid>')
def getImage(imageid):
    try:
        # 根目录imamges文件夹下 {}是匹配的意思
        image = file("images/{}.jpg".format(imageid))
        resp = Response(image, mimetype="image/jpeg")
        return resp
    except Exception, e:
        return jsonify({'error': 'error the image path'})

        # 第二种方式也可以实现 但是不知道这两种的区别
        # with open('image/' + str(imageid) + '.jpg') as f:
        #     return Response(f.read(), mimetype='image/jpeg')

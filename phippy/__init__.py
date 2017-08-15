# -*- coding: utf-8 -*-
import os

from flask import request
from flask import Flask, render_template, jsonify, send_from_directory, Response
from sqlalchemy import create_engine, desc, Integer, Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.utils import secure_filename

app = Flask(__name__)

from users import user as user_blurprint
from merchant import merchant as merchant_blurprint

app.register_blueprint(user_blurprint, url_prefix='/user')
app.register_blueprint(merchant_blurprint, url_prefix='/merchant')


engine = create_engine('mysql://root:123456@127.0.0.1:3306/phippy?charset=utf8',
                       encoding="utf-8",
                       echo=False)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


@app.route('/forapp',methods=['GET','POST'])

# app初始化的时候调用

def forapp():

    return jsonify({"a":"b"})

# from users import views
# 得到商家（根据store_type区分是旅行社还是餐馆）
@app.route('/getstore', methods=['GET', 'POST'])
def findStore():
    if request.method != 'POST':
        return jsonify({"msg": "is not post"})

    store_type = request.form.get('store_type')
    stores = Store.query.filter(Store.store_type == store_type).all()
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
@app.route('/getarticle', methods=['GET', 'POST'])
def getarticle():
    if request.method != 'POST':
        return jsonify({"msg": "is not post"})

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
@app.route('/getgoods', methods=['POST'])
def getfood():
    if request.method != 'POST':
        return jsonify({"msg": "is not post"})

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


# 带测试
@app.route('/addgoods', methods=['GET', 'POST'])
def addgoods():
    store_id = request.form.get('store_id')
    name = request.form.get('name')
    price = request.form.get('price')
    publish_time = request.form.get('publish_time')
    publisher = request.form.get('publisher')

    stores = Store.query.filter(Store.store_id == store_id).all()

    # 判断 store_id 是否正确
    if (len(stores) != 1):
        return jsonify({'error': '错误'})

    # 降序排列
    goods = Goods.query.order_by(desc(Goods.goods_id)).limit(1)

    add_goods_id = 0
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


@app.route('/img', methods=['POST'])
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


@app.route('/imgs', methods=['POST'])
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
@app.route('/uploadedfile/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


##下载服务器图片
@app.route('/image/<imageid>')
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


###########################################################################################
###########################################################################################
###########################################################################################



###############################################################
###############################################################

# 定义商家对象:
class Store(Base):
    # 表的名字:
    __tablename__ = 't_store'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, default=1, unique=True, autoincrement=1)

    # 0.admin
    # 1是旅行社
    # 2是餐馆
    #  3.药店
    # 4.保养品
    # 5.个人
    store_type = Column(Integer)

    # 店名
    name = Column(String(50))

    # 商家展示图片
    img_url = Column(String(100))

    # 电话号
    phone_number = Column(String(18))

    # 微信号
    wechat = Column(String(30))

    # 配送时间
    deliver_time = Column(String(30))

    # 起送条件
    qisong_condition = Column(String(30))

    # 店家地址
    adress = Column(String(100))

    # 排行
    rank = Column(Integer)

    # 当前开业还是关业  （0 1）
    operating_status = Column(Integer)
    #
    # # 续费状态 什么时间过期
    expire_time = Column(String(20))

    # 最新的通知
    latest_notice = Column(String(50))


# 定义Tour_article对象:
class Article(Base):
    # 表的名字:
    __tablename__ = 't_article'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    store_id = Column(String(20))
    title = Column(String(20))
    content = Column(String(1000))
    time = Column(DateTime)
    img_url = Column(String(100))
    rank = Column(Integer)


# 定义商品:
class Goods(Base):
    # 表的名字:
    __tablename__ = 't_goods'

    # 表的结构:
    id = Column(Integer, primary_key=True)

    # 商品id
    goods_id = Column(Integer, unique=True)

    # 商店id
    store_id = Column(Integer)

    # 商品名
    name = Column(String(20))
    price = Column(String(15))

    # 商品排行
    rank = Column(Integer)

    # 商品图片url
    img_url = Column(String(60))

    # 发布时间
    publish_time = Column(String(20))

    # 发布人
    publisher = Column(String(20))

    # 备注
    remark = Column(String(120))

    # 描述
    describe = Column(String(100))


# 订单表
class Order(Base):
    __tablename__ = 't_order'
    id = Column(Integer, primary_key=True)
    # 订单ID
    order_id = Column(String(20))
    # 下单时间
    order_time = Column(DateTime)
    # 提交人
    submitted_by = Column(String(16))
    # 订单类型
    order_type = (Integer)
    # 商店ID
    store_id = Column(Integer)
    # 订单状态
    order_status = Column(Integer)
    # 订单金额
    order_price = Column(Float)

# 订单商品列表
class OrderDetailList(Base):
    __tablename__ = 't_orderDetailList'
    id = Column(Integer, primary_key=True)
    # 订单ID (设置为外键)
    order_id = Column(String(20))

class Sequence(Base):
    __tablename__ = 't_sequence'
    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer)
    name = Column(String(20))
    count = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    pwd = Column(String(120), unique=False)
    user_id = Column(String(40), unique=True)
    email = Column(String(120), unique=False)

    # 国籍
    nationality = Column(String(20), unique=False)

    # 注册时间
    register_time = Column(DateTime, unique=False)

    # 最后登录时间
    last_time = Column(DateTime, unique=False)


    status = Column(Integer, unique=False)
    uuid = Column(String(120), unique=False)
    device = Column(String(50), unique=False)
    code = Column(String(20))


def init_db():
    Base.metadata.create_all(bind=engine)

@app.route('/')
def hello_world():
    init_db()
    return render_template("phone_type.html")


# if __name__ == '__main__':
#     app.run('10.71.66.2', debug=True, port=5001)


# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
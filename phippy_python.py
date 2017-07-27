# -*- coding: utf-8 -*-

from flask import Flask, render_template
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify
from flask import request


app = Flask(__name__)
engine = create_engine('mysql://root:123456@127.0.0.1:3306/phippy?charset=utf8',
                       encoding="utf-8",
                       echo=False)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# from users import views
# 得到商家（根据store_type区分是旅行社还是餐馆）
@app.route('/getstore',methods=['GET','POST'])
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

# 得到旅行相关的文章
@app.route('/getarticle',methods=['GET','POST'])
def getarticle():

    if request.method != 'POST':
        return jsonify({"msg":"is not post"})

    articles = Article.query.filter().all()
    list = []
    for article in articles:
        dict = {}
        dict['store_id']    = article.store_id
        dict['title']     = article.title
        dict['content']   = article.content
        dict['time']      = article.time
        dict['img_url']   = article.img_url
        dict['rank']      = article.rank

        list.append(dict)
    return jsonify({"interface":"得到旅行相关的文章",'data':list})

# 得到餐品
@app.route('/getgoods',methods=['POST'])
def getfood():

    if request.method != 'POST':
        return jsonify({"msg":"is not post"})

    store_id = request.form.get('store_id')
    goods = Goods.query.filter(Goods.store_id == store_id).all()
    list = []
    for tmp in goods:
        dict = {}
        dict['goods_id']    = tmp.goods_id
        dict['store_id']     = tmp.store_id
        dict['name']   = tmp.name
        dict['price'] = tmp.price
        dict['rank'] = tmp.rank
        dict['img_url'] = tmp.img_url
        dict['publish_time'] = tmp.publish_time
        dict['publisher'] = tmp.publisher
        dict['remark'] = tmp.remark
        dict['describe'] = tmp.describe

        list.append(dict)

    return jsonify({"interface":"得到餐品",'data':list})


def log(func):
    def wrapper(*args, **kw):
        print 'call %s():' % func.__name__
        return func(*args, **kw)
    return wrapper

###############################################################
###############################################################

# 定义商家对象:
class Store(Base):
    # 表的名字:
    __tablename__ = 't_store'

    # 表的结构:
    id              = Column(Integer, primary_key=True)
    store_id        = Column(Integer, unique=True)

    # 0.admin
    # 1是旅行社
    # 2是餐馆
    #  3.药店
    # 4.保养品
    # 5.个人
    store_type      = Column(Integer)

    # 店名
    name            = Column(String(50))

    # 商家展示图片
    img_url         = Column(String(100))

    # 电话号
    phone_number    = Column(String(18))

    # 微信号
    wechat          = Column(String(30))

    # 配送时间
    deliver_time    = Column(String(30))

    # 起送条件
    qisong_condition = Column(String(30))

    # 店家地址
    adress            = Column(String(100))

    # 排行
    rank            = Column(Integer)

   #当前开业还是关业  （0 1）
    # operating_status = Column(Integer)
    #
    # # 续费状态 什么时间过期
    # expire_time   = Column(String)


# 定义Tour_article对象:
class Article(Base):
    # 表的名字:
    __tablename__ = 't_article'

    # 表的结构:
    id          = Column(Integer, primary_key=True)
    store_id      = Column(String(20))
    title       = Column(String(20))
    content     = Column(String(1000))
    time        = Column(DateTime)
    img_url     = Column(String(100))
    rank        = Column(Integer)


# 定义商品:
class Goods(Base):
    # 表的名字:
    __tablename__ = 't_goods'

    # 表的结构:
    id         = Column(Integer, primary_key=True)

    # 商品id
    goods_id    = Column(Integer, unique=True)

    # 商店id
    store_id   = Column(Integer)

    # 商品名
    name      = Column(String(20))
    price = Column(String(15))

    # 商品排行
    rank = Column(Integer)

    # 商品图片url
    img_url     = Column(String(60))

    # 发布时间
    publish_time = Column(String(20))

    # 发布人
    publisher = Column(String(20))

    # 备注
    remark = Column(String(120))

    # 描述
    describe = Column(String(100))



def init_db():
    Base.metadata.create_all(bind=engine)

@app.route('/')
def hello_world():
    init_db()
    return render_template("phone_type.html")


if __name__ == '__main__':
    app.run('10.71.66.2',debug=True)

# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
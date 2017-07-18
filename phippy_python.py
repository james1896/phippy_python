# -*- coding: utf-8 -*-
from flask import Flask, render_template
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify


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
@app.route('/findstore',methods=['GET','POST'])
def findStore():
    stores = Store.query.filter().all()
    list = []
    for store in stores:
        dict = {}
        dict['store_id']        = store.store_id
        dict['store_type']      = store.store_type
        dict['name']            = store.name
        dict['phone_number']    = store.phone_number
        dict['adress']          = store.adress
        dict['rank']            = store.rank
        dict['rec_article_id']  = store.rec_article_id
        list.append(dict)
    return jsonify({"interface":"得到商家",'data':list})

# 得到旅行相关的文章
@app.route('/getarticle',methods=['GET','POST'])
def getarticle():
    articles = Tour_article.query.filter().all()
    list = []
    for article in articles:
        dict = {}
        dict['author']    = article.author
        dict['title']     = article.title
        dict['content']   = article.content
        dict['time']      = article.time
        dict['img_url']   = article.img_url
        dict['rank']      = article.rank

        list.append(dict)
    return jsonify({"interface":"得到旅行相关的文章",'data':list})

# 得到餐品
@app.route('/getfood',methods=['GET','POST'])
def getfood():
    articles = Food_article.query.filter().all()
    list = []
    for article in articles:
        dict = {}
        dict['food_id']    = article.food_id
        dict['store_id']     = article.store_id
        dict['title']   = article.title
        dict['time']      = article.time
        dict['price']   = article.price
        dict['rank']      = article.rank

        list.append(dict)
    return jsonify({"interface":"得到餐品",'data':list})




###############################################################
###############################################################

# 定义商家对象:
class Store(Base):
    # 表的名字:
    __tablename__ = 'store'

    # 表的结构:
    id              = Column(Integer, primary_key=True)
    store_id        = Column(Integer, unique=True)

    # 1是旅行社
    # 2是餐馆
    store_type      = Column(Integer)
    name            = Column(String(50))
    phone_number    = Column(String(20))
    adress            = Column(String(100))
    rank            = Column(Integer)
    rec_article_id  = Column(Integer)

# 定义Tour_article对象:
class Tour_article(Base):
    # 表的名字:
    __tablename__ = 'tour_article'

    # 表的结构:
    id          = Column(Integer, primary_key=True)
    author      = Column(String(20))
    title       = Column(String(20))
    content     = Column(String(1000))
    time        = Column(DateTime)
    img_url     = Column(String(100))
    rank        = Column(Integer)


# 定义Food_article对象:
class Food_article(Base):
    # 表的名字:
    __tablename__ = 'store_food'

    # 表的结构:
    id         = Column(Integer, primary_key=True)
    food_id    = Column(Integer, unique=True)
    store_id   = Column(Integer)
    title      = Column(String(20))
    time       = Column(DateTime)
    price    = Column(String(15))
    rank            = Column(Integer)


def init_db():
    Base.metadata.create_all(bind=engine)

@app.route('/')
def hello_world():
    init_db()
    return render_template("phone_type.html")


if __name__ == '__main__':
    app.run(debug=True)

# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
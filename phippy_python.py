# -*- coding: utf-8 -*-
from flask import Flask
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

@app.route('/findstore',methods=['GET','POST'])
def findStore():
    store = Store.query.filter().first()
    print store.name
    return jsonify({"a":"b"})


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
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
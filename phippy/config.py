# -*- coding: utf-8 -*-

# 配置数据库
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# _*_ coding: utf-8 _*_

#调试模式是否开启
DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/phippy?charset=utf8"
#
# engine = create_engine("mysql://root:123456@127.0.0.1:3306/phippy?charset=utf8",
#                        encoding="utf-8",
#                        echo=False)
#
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
# def init_db():
#     Base.metadata.create_all(bind=engine)
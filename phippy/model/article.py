# -*- coding: utf-8 -*-

# 定义Tour_article对象:
from sqlalchemy import Column, Integer, String, DateTime

from phippy import Base


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
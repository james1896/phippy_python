# -*- coding: utf-8 -*-

# 定义商品:
from sqlalchemy import Integer, Column, String

from phippy import Base


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

    # 当前开是否接收线上订餐  （0 1）
    online_order = Column(Integer)
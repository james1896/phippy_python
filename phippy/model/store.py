# -*- coding: utf-8 -*-

# 定义商家对象:
from sqlalchemy import Column, Integer, String

from phippy import Base



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

    # 店主名字
    shopkeeper_name = Column(String(8))

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

    # 当前开是否接收线上订餐  （0 1）
    online_order = Column(Integer)
    #
    # # 续费状态 什么时间过期
    expire_time = Column(String(20))

    # 最新的通知
    latest_notice = Column(String(50))
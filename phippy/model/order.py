# -*- coding: utf-8 -*-

# 订单表
from sqlalchemy import Column, Integer, String, DateTime, Float

from phippy import Base


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
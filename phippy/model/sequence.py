# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from phippy import Base


class Sequence(Base):
    __tablename__ = 't_sequence'
    id = Column(Integer, primary_key=True)

    # 商家添加商品的时候 +1
    goods_id = Column(Integer)


    name = Column(String(20))
    count = Column(Integer)
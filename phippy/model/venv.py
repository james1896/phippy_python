# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from phippy import Base


class Venv(Base):
    __tablename__ = 't_venv'
    id      = Column(Integer, primary_key=True)

    # 用户app版本号
    version_user = Column(String(10))
    # 商家app版本号
    version_merchant = Column(String(10))
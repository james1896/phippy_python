# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Column, DateTime

from phippy import Base


class User(Base):
    __tablename__ = 't_users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    pwd = Column(String(120), unique=False)
    user_id = Column(String(40), unique=True)
    email = Column(String(120), unique=False)

    # 国籍
    nationality = Column(String(20), unique=False)

    # 注册时间
    register_time = Column(DateTime, unique=False)

    # 最后登录时间
    last_time = Column(DateTime, unique=False)


    status = Column(Integer, unique=False)
    uuid = Column(String(120), unique=False)
    device = Column(String(50), unique=False)
    code = Column(String(20))
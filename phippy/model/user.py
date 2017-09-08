# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Column, DateTime, Float

from phippy import Base


class User(Base):
    __tablename__ = 't_users'

    id          = Column(Integer, primary_key=True)
    user_name   = Column(String(50), unique=True)
    pwd         = Column(String(120), unique=False)
    user_id     = Column(String(40), unique=True)
    phonen_umber = Column(String(20), unique=False)
    money       = Column(Float, unique=False)
    points      = Column(Float, unique=False)
    email       = Column(String(30), unique=False)

    # 国籍
    nationality = Column(String(20), unique=False)

    # 注册时间
    register_time = Column(DateTime, unique=False)

    # 最后登录时间
    last_time = Column(DateTime, unique=False)


    # 用户状态
    # 0 正常
    # 1 冻结
    # 2 删除
    status = Column(Integer, unique=False)


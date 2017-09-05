# -*- coding: utf-8 -*-

#########################   用户反馈 表结构    #####################################################
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from phippy import Base


class FeedBack(Base):
    __tablename__ = 't_feedback'
    id      = Column(Integer, primary_key=True)
    time    = Column(DateTime, unique=False)
    content = Column(String(500), unique=False)

    user_id = Column(Integer, ForeignKey('t_users.id'))

    def __init__(self,time = None,content = None,user_id = None):
        self.time       = time
        self.content    = content
        self.user_id    = user_id
# -*- coding: utf-8 -*-

#########################   用户设备管理 表结构    #####################################################
from sqlalchemy import Column, Integer, String, DateTime

from phippy import Base


class Userbehaviour(Base):
    __tablename__ = 't_behaviour'

    id          = Column(Integer, primary_key=True)
    username    = Column(String(20), unique=False)
    ip          = Column(String(20), unique=False)
    time        = Column(DateTime, unique=False)
    uuid        = Column(String(120), unique=False)
    platform    = Column(String(10), unique=False)
    device      = Column(String(50), unique=False)
    version     = Column(String(8), unique=False)
    language    = Column(String(15), unique=False)


    # user_id     = Column(Integer, ForeignKey('users.id'))

    def __init__(self):
        print "init userbehaviour"

    def __init__(self, last_time=None, username=None,uuid=None,device=None):

        self.username    = username
        self.last_time  = last_time
        self.uuid       = uuid
        self.device     = device
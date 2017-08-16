# -*- coding: utf-8 -*-
import os

from flask import request
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from phippy.config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

# rsa解密
# def decryption(encode_value):
#     return rsaCipher.decryptionWithString(encode_value, random_generator)
# # 解密成string
# decodeStr = decryption(value)
# # jsonn --> dictt
# value_dict = json.loads(decodeStr)

#加载配置文件内容
app.config.from_object('phippy.config')     #模块下的setting文件名，不用加py后缀



# 创建实例，并连接test库
# echo=True 显示信息
engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       encoding="utf-8",
                       echo=False)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# 生成orm基类
Base = declarative_base()
Base.query = db_session.query_property()


# 注册蓝图
from users.user import user as user_blurprint
from merchant.merchant import merchant as merchant_blurprint

app.register_blueprint(user_blurprint, url_prefix='/user')
app.register_blueprint(merchant_blurprint, url_prefix='/merchant')




@app.route('/')
def hello_world():
    init_db()
    return render_template("phone_type.html")


@app.route('/forapp',methods=['GET','POST'])

# app初始化的时候调用

def forapp():

    return jsonify({"a":"b"})


###########################################################################################
###########################################################################################
###########################################################################################



###############################################################
###############################################################




def init_db():
    Base.metadata.create_all(bind=engine)


# if __name__ == '__main__':
#     app.run('10.71.66.2', debug=True, port=5001)


# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
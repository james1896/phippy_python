# -*- coding: utf-8 -*-

from phippy_python import app
from flask import jsonify

@app.route('/findstore',methods=['GET','POST'])
def findStore():
    return jsonify({"a":"b"})

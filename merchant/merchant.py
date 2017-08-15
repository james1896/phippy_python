# -*- coding: utf-8 -*-

from flask import Blueprint
merchant    = Blueprint('merchant',__name__)

@merchant.route('/')
def app_index():
    return 'hello merchant'
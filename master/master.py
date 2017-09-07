# -*- coding: utf-8 -*-

from . import master

@master.route('/')
def app_index():
    return 'hello master'
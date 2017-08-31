# -*- coding: utf-8 -*-
from . import common

@common.route('/')
def app_index():
    return 'hello common'
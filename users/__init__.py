# -*- coding: utf-8 -*-

from flask import Blueprint

user        = Blueprint("user",__name__)
merchant    = Blueprint("maerchant",__name__)

from . import user
from . import merchant
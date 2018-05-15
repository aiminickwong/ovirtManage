# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import  Blueprint

auth = Blueprint('auth',__name__)


from . import account_view

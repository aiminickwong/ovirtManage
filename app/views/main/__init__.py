# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import  Blueprint

main = Blueprint('main',__name__)


from  . import index_view

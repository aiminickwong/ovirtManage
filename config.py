# -*- coding:utf-8 -*-
__author__ = 'xuan'

import  os



class Config:
    SECRET_KEY  = os.environ.get('SECRET_KEY') or '\x86pR6\xa28\x95\x03Ml\xb8\x89\xba\x9a\xc5\x7fD\xe6\x03\x14m0\xcb'
    SQLALCHEMY_COMMIT_ON_TEARDOWM = True
    #配置邮件
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_MAIL_SENDER = os.environ.get('ADMIN_MAIL_SENDER')
    ADMIN_MAIL = os.environ.get('ADMIN_MAIL')

    MYSQL_PWD = os.environ.get('MYSQL_PWD')
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    
    #文件上传
    UPLOAD_FOLDER = '/home/iso_file'
    THUMBNAIL_FOLDER = 'app/static/data/thumbnail'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024 * 1024

  
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_RUL') or \
        'mysql://root:uroot012@localhost:8808/ovirt_development'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql://root:uroot012@localhost:8808/ovirt_testing'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
         'mysql://root:uroot012@localhost:8808/ovirt_production'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

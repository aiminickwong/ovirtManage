# -*- coding:utf-8 -*-
__author__ = 'xuan'

# from  . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
# from .import login_manager
# from app import login_manager

from flask_login import LoginManager




db = SQLAlchemy()
login_manager = LoginManager()

login_manager.session_protection = 'strong'

'''当蓝本名字修改时这里也要修改'''
login_manager.login_view = 'auth.login'


registrations =  db.Table('registrations',
        db.Column('users_id',db.Integer,db.ForeignKey('users.id')),
        db.Column('roles_id',db.Integer,db.ForeignKey('roles.id'))
)



class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',
                            secondary=registrations,
                            backref=db.backref('roles',lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property #相当于get_password
    def password(self):
        raise AttributeError('password is not readable attribute')

    '''
    当用shell插入User模型时，不用password_hash，直接用password=.....
    '''
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User_List(db.Model):
    __tablename__='user_list'
    id = db.Column(db.String(128),primary_key=True)
    name = db.Column(db.String(64),unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    displayname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    department = db.Column(db.String(64))
    title = db.Column(db.String(64))
    description = db.Column(db.String(64))
    accountDisabled = db.Column(db.String(64))
    accountUnlockedAt = db.Column(db.String(64))
                                                                       
    def __repr__(self):
        return '<User_List %r>' % self.name


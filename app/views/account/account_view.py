# -*- coding:utf-8 -*-
__author__ = 'xuan'

from  flask import  render_template,request,redirect,url_for,flash
from . import  auth
from flask_login import logout_user,login_required,login_user,current_user
from ...models  import User,Role
from flask_principal import Identity,AnonymousIdentity,identity_changed,current_app





@auth.route('/',methods=['GET','POST'])

def login():
    if request.method == 'POST':
    
        if 'Username' in request.form:
            username = request.form['Username']
        else:
            username = ''

        if 'Password' in request.form:
            password = request.form['Password']
        else:
            password = ''

        user = User.query.filter_by(username=username).first()
        #print user
        if user is not None and user.verify_password(password):
            # if user.username =='admin':
            #     login_user(user)
            #     return redirect(request.args.get('next') or '/admin')
            # else:
            login_user(user)
            # identity_changed.send(current_app._get_current_object(),
            #                       identity=Identity(user.id)
            #                       )
            return redirect(request.args.get('next') or url_for('main.users'))
        flash(u'无效的帐户或密码')



    return render_template('account/login.html')


@auth.route('/logout',methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    # identity_changed.send(
    #     current_app._get_current_object(),
    #     identity=AnonymousIdentity()
    # )
    flash(u'已退出登录')
    return redirect(url_for('auth.login'))

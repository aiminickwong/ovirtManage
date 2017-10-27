# -*- coding:utf-8 -*-
__author__ = 'xuan'

import  os

from app import create_app

from app.models  import db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app.models import Role,User
#from flask_admin import Admin
# from app import my_admin
# from app.admin.admin import MyView
# from flask_admin import BaseView,expose

# from flask.ext.admin.contrib.sqla import ModelView




app = create_app(os.getenv('FLASK_CONFIG') or 'default')  #export的时候 输入export FLASK_CONFIG=development
manager = Manager(app)
migrate = Migrate(app,db)


# class MyView(BaseView):
 
#     # @admin.expose('/')
#     @expose('/')    
#     def index(self):
#         print 'admin'
#         return self.render('admin/custom.html')

#my_admin.add_view
#my_admin.add_view(MyView(name='myview'))
#my_admin.add_view(ModelView(User,db.session))    


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    '''Run the unit tests'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()



# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import render_template,request,current_app,session,redirect,url_for,send_from_directory,flash
from . import  main
from  manage import  db
from  manage import app
import commands
import sys,json
import simplejson
from flask.ext.login import login_required, current_user, login_user, logout_user
from more_itertools import chunked
import os
import difflib
from config import config
from lib.upload_file import uploadfile
from werkzeug.utils import secure_filename
from datetime import datetime
import time
import re
import MySQLdb
from  multiprocessing import Pool
import binascii
import shutil

reload(sys)
sys.setdefaultencoding('utf8')


@main.route('/users',methods=['GET','POST'])
@login_required
def users():
    if request.method == 'POST':
        #新建用户
        data = request.form.get('data', '')
        #any判断一个对象是否为空的方法
        if  any(data):
            print '新建用户:',data
            try:
                form_data=json.loads(data)["data"]
                name =  form_data['name']
                firstname = form_data['firstname']
                lastname = form_data['lastname']
                if name !='':
                    message = commands.getstatusoutput('ovirt-aaa-jdbc-tool user add %s'%(name))

                return simplejson.dumps({"message": message})
            except:
                print 'None'
        else:
            print 'None'


        #删除用户
        del_user = request.form.get('del_user', '')
        if any(del_user):
            print 'del_user',del_user
            del_user_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool user delete %s'%(del_user))
            print del_user_message

            return simplejson.dumps({"message": del_user_message})
        else:
            print 'None'

        #删除多个用户
	    del_users = request.form.get('delete_users','')
        if any(del_users):
            try:
                del_users_list=json.loads(del_users)["data"]

                for users in del_users_list:
                    del_users_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool user delete %s'%(users))

            except:
                print 'except'


        #解锁用户
        unlock_user = request.form.get('unlock_user', '')
        if any(unlock_user):
            unlock_user_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool user unlock %s'%(unlock_user))

            return simplejson.dumps({"message": unlock_user_message})
        else:
            print 'None'

        #设置密码
        set_pwd_name = request.form.get('set_pwd_name', '')
        set_pwd = request.form.get('set_pwd', '')
        if any(set_pwd) and any(set_pwd_name):
            print 'set_pwd'
            set_pwd_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool user password-reset %s --password=pass:%s --password-valid-to="2030-12-31 10:30:00Z" '%(set_pwd_name,set_pwd))
            #print set_pwd_message

            return simplejson.dumps({"message": set_pwd_message})
        else:
            print 'None'
            return simplejson.dumps({"message": 'None'})

        #修改密码
        # change_pwd_name = request.form.get('change_pwd_name', '')
        # change_pwd = request.form.get('change_pwd', '')
        # if any(change_pwd_name) and any(change_pwd):
        #     print 'change_pwd'
        #     change_pwd_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool user password-reset %s  --password=pass:%s'%(change_pwd_name,change_pwd))
        #     print change_pwd_message
        #
        #     return simplejson.dumps({"message": change_pwd_message})
        # else:

    else:
        return render_template('index/users.html')

@main.route('/users_return_json',methods=['GET','POST'])
@login_required
def users_return_json():

    file_name = '%s/app/static/users.txt'%os.getcwd()

    all_users = commands.getstatusoutput('ovirt-aaa-jdbc-tool query --what=user |grep -wE "ID|Name|Email|Department|Title|Description|Disabled|Unlocked At"')

    with open(file_name, 'wb') as f:
         f.write(all_users[1])

    result = []
    with open(file_name) as f:
        for i in f.readlines():
            tmp = i.strip().split(':', 1)  # 只切割一次
    	    result.append(tmp)

            rs =  [x for x in chunked(result,11)]

        jsonData = []
        for i in range(len(rs)):
            di = {}
            for k,v in enumerate(rs[i]):
                if v !=['']:
                    di[v[0]] = v[1]
                    if k ==10:
                        jsonData.append(di)

        # print '最终返回',jsonData
    return  json.dumps(jsonData)


@main.route('/user_group',methods=['GET','POST'])
@login_required
def user_group():
    if request.method == 'POST':

        #用户加入到用户组
        add_to_group_data = request.form.get('add_to_group_data', '')

        if any(add_to_group_data):

            select_users = json.loads(add_to_group_data)["select_users"]
            select_users = select_users

            try:
                form_data=json.loads(add_to_group_data)["data"]
                group =  form_data['group']

                if group  !=' ':
                    for i in select_users:
                        add_to_group_terminal_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool group-manage useradd %s --user=%s'%(group,i))

                    user_member = commands.getstatusoutput('ovirt-aaa-jdbc-tool group-manage show %s | grep -wE "User"'%(group.strip()))

                    file_name = '%s/app/static/group_member.txt'%os.getcwd()

                    #写文件
                    with open(file_name, 'wb') as f:
                        f.write(user_member[1])

                    return simplejson.dumps({"message": add_to_group_terminal_message })
            except:
                print 'exceptNone'
        else:
            print 'None'



        data = request.form.get('data', '')
        #any判断一个对象是否为空的方法
        if  any(data):
            print '新建用户组:',data
            try:
                form_data=json.loads(data)["data"]
                group =  form_data['group']
                description =  form_data['description']

                if group and description  !='':
                    add_usergroup_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool group add %s  --attribute="description=%s" '%(group,description))
                return simplejson.dumps({"message": add_usergroup_message})
            except:
                print 'None'
        else:
            print 'None'

        #删除用户组
        del_user_group = request.form.get('del_user_group', '')
        if any(del_user_group):
            del_user_group_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool group delete %s'%(del_user_group))

            return simplejson.dumps({"message": del_user_group_message})
        else:
            print 'None'

        #return simplejson.dumps({"message": 'None'})

    else:
        return render_template('index/user_group.html')


@main.route('/user_group_return_json',methods=['GET','POST'])
@login_required
def user_group_return_json():

    file_name = '%s/app/static/user_group.txt'%os.getcwd()

    all_user_group = commands.getstatusoutput('ovirt-aaa-jdbc-tool query --what=group |grep -wE "ID|Name|Description"')

    with open(file_name, 'wb') as f:
        f.write(all_user_group[1])

    result = []
    with open(file_name) as f:
        for i in f:
            tmp = i.strip().split(':', 1)  # 只切割一次
    	    result.append(tmp)
            #每4个为一个组
            rs =  [x for x in chunked(result,4)]

        jsonData = []
        for i in range(len(rs)):
            di = {}
            for k,v in enumerate(rs[i]):
                if v !=['']:
                    di[v[0]] = v[1]
                    if k == 3:
                        jsonData.append(di)

    return  json.dumps(jsonData)

@main.route('/user_group_member',methods=['GET','POST'])
@login_required
def user_group_member():
    group_mem = request.args.get("group")

    if request.method == 'POST':
        file_name = '%s/app/static/group_member.txt'%os.getcwd()
        remove_user = request.form.get('remove_user', '')
        group = request.form.get('group')
        if any(remove_user) and any(group):

            remove_user_message = commands.getstatusoutput('ovirt-aaa-jdbc-tool group-manage userdel %s --user=%s'%(group,remove_user.strip()))

            user_member = commands.getstatusoutput('ovirt-aaa-jdbc-tool group-manage show %s | grep -wE "User"'%(group.strip()))

            write_member = user_member[1]

            if user_member[1] == '':
                write_member='''
                                User: -
                             '''
            #写文件
            with open(file_name, 'wb') as f:
                f.write(write_member)

    return render_template('index/user_group_member.html',group_mem=group_mem)



@main.route('/user_group_member_return_json',methods=['GET','POST'])
@login_required
def user_group_member_return_json():
    file_name = '%s/app/static/group_member.txt'%os.getcwd()
    if request.method == 'POST':

        find_group = request.form.get('find_group', '')

        if find_group !='':

            user_member = commands.getstatusoutput('ovirt-aaa-jdbc-tool group-manage show %s | grep -wE "User"'%(find_group.strip()))

            write_member = user_member[1]

            if user_member[1] == '':
                write_member='''
                                User: -
                             '''
            #写文件
            with open(file_name, 'wb') as f:
                f.write(write_member)

    result = []
    with open(file_name) as f:
        for i in f:
            tmp = i.strip().split(':', 1)  # 只切割一次
    	    result.append(tmp)
            #每1个为一个组
            rs =  [x for x in chunked(result,1)]
        jsonData = []
        for i in range(len(rs)):
            di = {}
            for k,v in enumerate(rs[i]):
                if v !=['']:
                    di[v[0]] = v[1]
                    if k == 0:
                        jsonData.append(di)

    return  json.dumps(jsonData)


#添加到用户组时需要加载的用户列表
@main.route('/user_load_return_json',methods=['GET','POST'])
@login_required
def load_users():
    file_users = '%s/app/static/users.txt'%os.getcwd()
    filter_list = '%s/app/static/filter_list.txt'%os.getcwd()
    file_load_users = '%s/app/static/load_users.txt'%os.getcwd()

    if not os.path.exists(filter_list):
        print '不存在，新建文件'
        f = open(filter_list,'w')
        f.close()

    if request.method == 'POST':
        #load

        query_group = request.form.get('query_group', '')

        if any(query_group):
            group = json.loads(query_group)["data"]
            group_member = commands.getstatusoutput('ovirt-aaa-jdbc-tool group-manage show %s | grep -wE "User"'%(group.strip()))

            filters = group_member[1].replace(' ', '').splitlines(1)

            get_filters = []
            for i in filters:
                line = i.strip('\n')
                get_filters.append(line)

            all_users = commands.getstatusoutput('ovirt-aaa-jdbc-tool query --what=user |grep -wE "^Name"')

        get_users = []

        all_users = all_users[1].replace(' ','').splitlines(1)
        for line in all_users:
            get_users.append(line.replace('Name','User').strip('\n'))

        ret = list(set(get_users) ^ set(get_filters))

        result = []
        for i in ret:
            tmp = i.split(":",1)
            result.append(tmp)

        rs = [x for x in chunked(result,1)]
        jsonData = []

        try:
            for i in range(len(rs)):
                    di = {}
                    for k,v in enumerate(rs[i]):
                        if k == 0 and v !=[''] :
                            json.dumps(jsonData)
                            di['id'] = i
                            di['text'] = v[1]

                            jsonData.append(di)
        except:
            return  simplejson.dumps({"errmessage": '无可加入用户！'})

	print(jsonData)
        return  json.dumps(jsonData)


#返回终端机可加入的组
@main.route('/group_load_return_json',methods=['GET','POST'])
@login_required
def load_group():
    if request.method == 'POST':
        db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
        cursor = db.cursor()

     	search_sql =  "SELECT GROUP_NAME from groupmanage"

        try:
            cursor.execute(search_sql)
            data = cursor.fetchall()

            jsonData = []
            for n, row in enumerate(data):
                result = {}
                result['text'] = row[0]
                result['id'] = n

                jsonData.append(result)

            return json.dumps(jsonData)
        except:
            db.rollback()



#返回终端机信息
@main.route('/machine_load_return_json',methods=['GET','POST'])
@login_required
def load_machines():
    if request.method == 'POST':
        db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
        cursor = db.cursor()

        search_sql =  "SELECT * from assets"

        try:
            cursor.execute(search_sql)
            data = cursor.fetchall()

            jsonData = []
            for n, row in enumerate(data):
                result = {}
                result['text'] = row[16]
		result['id'] = n

                jsonData.append(result)


            return json.dumps(jsonData)
        except:
            db.rollback()



ALLOWED_EXTENSIONS = set(['iso','txt','sql'])
IGNORED_FILES = set(['.gitignore'])


# 上传文件允许的类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 生成文件名
def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    print '生成文件名', os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)
    i = 1
    while os.path.exists(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


@main.route("/upload",methods=['GET','POST'])
@login_required
def iso_upload():
    if not os.path.exists('/home/iso_file'):
        os.mkdir('/home/iso_file')

    if request.method == 'POST':
        print 'upload iso'
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):

                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="不支持的文件类型")


            else:
                # save file to disk  os.getcwd()获取当前脚本路径
                print "保存文件", os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print "uploaded_file_path", uploaded_file_path
                file.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # 在saving后保存上传日期和路径
                # 获取系统时间
                #get_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                #print '----',datetime.utcnow()
                #upload_date = get_time

                if '.' in filename:
                    number = filename.rsplit('.', 1)[0]

                # add_contract = Contract(name=filename, path=uploaded_file_path, upload_date=get_time, number=number)
                # db.session.add(add_contract)
                # db.session.commit()

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        print "GET"



        # get all file in ./data directory
        files = [f for f in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'])) if
                 os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)) and f not in IGNORED_FILES]

        file_display = []
        #get_time = datetime.utcnow()

        for f in files:
            # 获取每个iso文件的上传日期
            # if Contract.query.filter_by(name=f).first() is not None:
            #     upload_date_display = Contract.query.filter_by(name=f).first().upload_date
            # else:
            #     upload_date_display = '-'

            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size) #upload_date=upload_date_display
            file_display.append(file_saved.get_file())
        return simplejson.dumps({"files": file_display})

    return redirect(url_for('main.iso_file'))

@main.route("/delete/<string:filename>", methods=['DELETE'])
@login_required
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(os.getcwd(),app.config['THUMBNAIL_FOLDER'], filename)


    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@main.route("/thumbnail/<string:filename>", methods=['GET'])
@login_required
def get_thumbnail(filename):
    print "获取静态文件", app.config['THUMBNAIL_FOLDER']
    print "获取静态文件", filename

    return send_from_directory(os.path.join(os.getcwd(),app.config['THUMBNAIL_FOLDER']), filename=filename)


@main.route("/data/<string:filename>", methods=['GET'])
@login_required
def get_file(filename):
    print "获取上传文件：", filename
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename=filename)


@main.route('/iso_file', methods=['GET', 'POST'])
@login_required
def iso_file():
    return render_template('index/iso_file.html')


@main.route('/change_ip', methods=['GET', 'POST'])
@login_required
def change_ip():

    ifcfg = '/etc/sysconfig/network-scripts/ifcfg-ovirtmgmt'
    route = '/etc/sysconfig/network-scripts/route-ovirtmgmt'
    host = '/etc/hosts'

    ip_mask_gate = []
    with open(ifcfg) as f:
        for line in f.readlines():
	    if(line.find('IPADDR')==0):
	        ipaddr = line.strip().split('=',1)
		ip_mask_gate.append(ipaddr[1])
            if(line.find('NETMASK')==0):
		netmask = line.strip().split('=',1)
		ip_mask_gate.append(netmask[1])
	    if(line.find('GATEWAY')==0):
		gateway = line.strip().split('=',1)
		ip_mask_gate.append(gateway[1])



    #显示hostname
    hostname = commands.getstatusoutput('hostname')[1]

    if request.method == 'POST':

	#flash(u'正在重启服务')

	re_data = request.form.get('data', '')
	if any(re_data):
	    try:
	        form_data = json.loads(re_data)["data"]
                ipaddr = form_data['ipaddr']
        	netmask = form_data['netmask']
        	gateway = form_data['gateway']

    	    	data = ''

	    	if ipaddr != "" and netmask !="" and gateway != "":
		    print '修改ifcfg-ovirtmgmt'
    	    	    with open(ifcfg) as f:
                        for line in f.readlines():
    	                    if(line.find('IPADDR')==0):
	    	                line = 'IPADDR=%s'%(ipaddr) + '\n'
			    if(line.find('NETMASK')==0):
				line = 'NETMASK=%s'%(netmask) + '\n'
			    if(line.find('GATEWAY')==0):
				line = 'GATEWAY=%s'%(gateway) + '\n'

	                    data += line

                    with open(ifcfg,'w') as f:
	               f.writelines(data)


		    print '修改route-ovirtmgmt'

		    route_data = ''
		    with open(route) as f:
			for line in f.readlines()[:2]:
			    route_data += line


                    with open(route) as f:
			for line in f.readlines()[2:]:
		            #get_line = line.split(' ')
			    pattern = 'via (.*?) dev'
			    out = re.sub(pattern,'via %s dev'%ipaddr,line)
			    route_data += out

                    with open(route,'w') as f:
                        f.writelines(route_data)

		    print '修改host'
		    host_data = ''
		    with open(host) as f:
                       lines = f.readlines()

                    pattern = r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'
                    out = re.sub(pattern,'%s'%ipaddr,lines[2])

		    lines[-1] = out


                    with open(host,'w') as f:
                        f.writelines(lines)

		    network = commands.getstatusoutput('service network restart')
		    #ovirtengine = commands.getstatusoutput('service ovirt-engine restart')


	    except Exception as e:
		print e


    return render_template('index/change_ip.html',ipaddr=ip_mask_gate[0],netmask=ip_mask_gate[1],gateway=ip_mask_gate[2],hostname=hostname)


import multiprocessing
import socket

@main.route('/server_ip', methods=['GET', 'POST'])
@login_required
def ret_server_ip():
    "获取IP地址"
    def get_local_ip(ifname = 'ovirtmgmt'):
        import socket, fcntl, struct
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
        ret = socket.inet_ntoa(inet[20:24])
        return ret

    server_ip =  get_local_ip()


    def novnc_pwd():
	with open("vnc/noVNC/vnc_lite.html",'r') as f:
    	    htmlstr = f.read()

	#获取终端密码
	get_vnc_pwd = request.form.get('vnc_pwd_data','')
	vnc_pwd = json.loads(get_vnc_pwd)["pwd"]

	html_output = re.sub(r'<input type=password size=10 id="password_input" class="noVNC_status" value="">','<input type=password size=10 id="password_input" class="noVNC_status" value="%s">'%(vnc_pwd),htmlstr)

        with open("vnc/noVNC/vnc_lite.html",'w') as fw:
    	    fw.write(html_output)

  	with open("vnc/noVNC/core/rfb.js",'r') as f:
	    jsstr = f.read()

	js_output = re.sub(r'this._rfb_password = "";','this._rfb_password = "%s";'%(vnc_pwd),jsstr)

	with open("vnc/noVNC/core/rfb.js",'w') as fw:
	    fw.write(js_output)

    novnc_pwd()

    return simplejson.dumps({"server_ip": server_ip})


@main.route('/remote', methods=['GET', 'POST'])
@login_required
def remote():

    if request.method == 'POST':

        db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
        cursor = db.cursor()

        create_assets_sql = """CREATE TABLE IF NOT EXISTS `assets` (
  	    	`CLIENT_MAC` VARCHAR(255),
 	    	`CLIENT_VNCPWD` VARCHAR(255),
  	    	`CLIENT_CFGPWD` VARCHAR(255),
  	    	`CLIENT_DFAPP` VARCHAR(255),
  	    	`CLIENT_DFSRV` VARCHAR(255),
 	    	`CLIENT_MEM` VARCHAR(255),
  	    	`CLIENT_GPU` VARCHAR(255),
  	    	`CLIENT_CPU` VARCHAR(255),
  	    	`CLIENT_NIC` VARCHAR(255),
  	    	`CLIENT_OS` VARCHAR(255),
  	    	`CLIENT_Model` VARCHAR(255),
  	    	`CLIENT_STORAGE` VARCHAR(255),
  	    	`CLIENT_KERNEL` VARCHAR(255),
  	    	`CLIENT_IP` VARCHAR(255),
  	    	`CLIENT_AUDIO` VARCHAR(255),
 	    	`CLIENT_VERSION` VARCHAR(255),
  	    	`CLIENT_NAME` VARCHAR(255),
  	    	`CLIENT_FREQ`  VARCHAR(255),
  	    	`CLIENT_DISPLAY` VARCHAR(255),
  	    	`CLIENT_OPT` VARCHAR(255),
  	        `CLIENT_SESSION_0_TYPE` VARCHAR(255),
 	   	    `CLIENT_LANGUAGE` VARCHAR(255),
  	   	 PRIMARY KEY(`CLIENT_MAC`)
	     )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        create_group_sql = """CREATE TABLE IF NOT EXISTS `groupmanage` (
  	    	`GROUP_NAME` VARCHAR(255),
 	    	`GROUP_REMARK` VARCHAR(255),

  	   	 PRIMARY KEY(`GROUP_NAME`)
	     )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        try:
            cursor.execute(create_assets_sql)
            cursor.execute(create_group_sql)
            db.commit()
        except:
            print('生成数据表出错')
            db.rollback()

        re_data = request.form.get('data', '')
        if any(re_data):
            try:
                form_data = json.loads(re_data)["data"]
                ipaddr_1 = form_data['ipaddr_1']
	        ipaddr_2 = form_data['ipaddr_2']
	        ipaddr_3 = form_data['ipaddr_3']

                if ipaddr_1 and ipaddr_2 and ipaddr_3 != "":
	     	    #print('run search...')

		    def search_task():
                        for i in range(1,255):
                            #print('Search... ip:%s'%i)
			    #这里不用commands命令,会出现问题
   		            search = os.popen('tcmclient  %s.%s.%s.%s --scani&'%(ipaddr_1,ipaddr_2,ipaddr_3,i))

	        search_task()

   	        print('search done')
            except Exception as e:
               print e

            def read_file(file_path):
                with open(file_path,'r') as f:
	            for line in f.readlines():
	                if(line.find('CLIENT_MAC')==0):
	                    CLIENT_MAC = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_VNCPWD')==0):
	                    CLIENT_VNCPWD = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_CFGPWD')==0):
	                    CLIENT_CFGPWD = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_DFAPP')==0):
	                    CLIENT_DFAPP = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_DFSRV')==0):
                            CLIENT_DFSRV = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_MEM')==0):
	                    CLIENT_MEM = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_GPU')==0):
	                    CLIENT_GPU = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_CPU')==0):
	                    CLIENT_CPU = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_NIC')==0):
	                    CLIENT_NIC = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_OS')==0):
	                    CLIENT_OS = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_Model')==0):
	                    CLIENT_Model = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_STORAGE')==0):
	                    CLIENT_STORAGE = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_KERNEL')==0):
	                    CLIENT_KERNEL = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_IP')==0):
	                    CLIENT_IP = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_AUDIO')==0):
	                    CLIENT_AUDIO = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_VERSION')==0):
	                    CLIENT_VERSION = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_NAME')==0):
	                    CLIENT_NAME = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_FREQ')==0):
	                    CLIENT_FREQ = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_DISPLAY')==0):
	                    CLIENT_DISPLAY = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_OPT')==0):
	                    CLIENT_OPT = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_SESSION_0_TYPE')==0):
	                    CLIENT_SESSION_0_TYPE = line.strip().split('=',1)[1]
                        if(line.find('CLIENT_LANGUAGE')==0):
	                    CLIENT_LANGUAGE = line.strip().split('=',1)[1]

                try:
                    cursor.execute("select 1 from assets where CLIENT_MAC = '%s' limit 1"%(CLIENT_MAC))
                    data = cursor.fetchone()
                except:
                    db.rollback()

	        update_sql = "update assets set CLIENT_VNCPWD='%s',CLIENT_CFGPWD='%s',CLIENT_DFAPP='%s',CLIENT_DFSRV='%s',CLIENT_MEM='%s',CLIENT_GPU='%s',CLIENT_CPU='%s',CLIENT_NIC='%s',CLIENT_OS='%s',CLIENT_Model='%s',CLIENT_STORAGE='%s',CLIENT_KERNEL='%s',CLIENT_IP='%s',CLIENT_AUDIO='%s',CLIENT_VERSION='%s',CLIENT_NAME='%s',CLIENT_FREQ='%s',CLIENT_DISPLAY='%s',CLIENT_OPT='%s',CLIENT_SESSION_0_TYPE='%s',CLIENT_LANGUAGE='%s' where CLIENT_MAC='%s'"%(str(CLIENT_VNCPWD),str(CLIENT_CFGPWD),str(CLIENT_DFAPP),str(CLIENT_DFSRV),str(CLIENT_MEM),str(CLIENT_GPU),str(CLIENT_CPU),str(CLIENT_NIC),str(CLIENT_OS),str(CLIENT_Model),str(CLIENT_STORAGE),str(CLIENT_KERNEL),str(CLIENT_IP),str(CLIENT_AUDIO),str(CLIENT_VERSION),str(CLIENT_NAME),str(CLIENT_FREQ),str(CLIENT_DISPLAY),str(CLIENT_OPT),str(CLIENT_SESSION_0_TYPE),str(CLIENT_LANGUAGE),str(CLIENT_MAC))

                insert_sql = "insert into assets(CLIENT_MAC,CLIENT_VNCPWD,CLIENT_CFGPWD,CLIENT_DFAPP,CLIENT_DFSRV,CLIENT_MEM,CLIENT_GPU,CLIENT_CPU,CLIENT_NIC,CLIENT_OS,CLIENT_Model,CLIENT_STORAGE,CLIENT_KERNEL,CLIENT_IP,CLIENT_AUDIO,CLIENT_VERSION,CLIENT_NAME,CLIENT_FREQ,CLIENT_DISPLAY,CLIENT_OPT,CLIENT_SESSION_0_TYPE,CLIENT_LANGUAGE,CLIENT_GROUP)" + 'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' %(str(CLIENT_MAC),str(CLIENT_VNCPWD),str(CLIENT_CFGPWD),str(CLIENT_DFAPP),str(CLIENT_DFSRV),str(CLIENT_MEM),str(CLIENT_GPU),str(CLIENT_CPU),str(CLIENT_NIC),str(CLIENT_OS),str(CLIENT_Model),str(CLIENT_STORAGE),str(CLIENT_KERNEL),str(CLIENT_IP),str(CLIENT_AUDIO),str(CLIENT_VERSION),str(CLIENT_NAME),str(CLIENT_FREQ),str(CLIENT_DISPLAY),str(CLIENT_OPT),str(CLIENT_SESSION_0_TYPE),str(CLIENT_LANGUAGE),"")

                if data is not None:
		    sql = update_sql
	            print('更新assets')
	        else:
		    sql = insert_sql
		    print('写入assets')

	        return sql

            def db_execute(sql):
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()

                # db.close()

            def write_vnc_tokens():
	        print('写入vnc_tokens')
                sql = "select CLIENT_NAME,CLIENT_IP from assets"
	        try:
	            cursor.execute(sql)
	            data = cursor.fetchall()
		    token_file = os.getcwd() + "/vnc/noVNC/vnc_tokens"
	      	    with open(token_file,'w') as f:
		        for row in data:
		            f.write("%s: %s:5900 \n"%(row[0],row[1]))

    	            cursor.close()
	        except:
	            db.rollback()

 	        db.close()

            def search_file():
                filenames = os.listdir('/var/lib/tftpboot/')
                if filenames != " ":
                    for filename in filenames:
                        sql_lines = read_file('/var/lib/tftpboot/%s'%filename)
                        db_execute(sql_lines)

            search_file()
	    print('搜索完成')
	    write_vnc_tokens()
            #return redirect(url_for('remote'))i

	#加入到用户组
	add_to_group_users = request.form.get('users_data', '')

	if any(add_to_group_users):

	    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            cursor = db.cursor()

	    groupName =  json.loads(add_to_group_users)["selected_group"]
	    select_users = json.loads(add_to_group_users)["select_users"]

	    print(groupName)
	    print(select_users)
            for i in select_users:
		try:
		    cursor.execute("UPDATE assets SET CLIENT_GROUP='%s' WHERE CLIENT_NAME='%s' "%(groupName,i))
	     	    db.commit()
		except:
		    db.rollback()

	#删除瘦客户机
	del_users = request.form.get('del_users', '')


        if any(del_users):

            db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            cursor = db.cursor()

	    users = json.loads(del_users)["del_users"]

	    for i in users:
                try:
		    print('删除')

                    cursor.execute("DELETE FROM assets WHERE CLIENT_NAME='%s' "%(i))
                    db.commit()
                except:
                    db.rollback()

	    #删除对应的瘦客户机文本文件
	    mac = json.loads(del_users)["select_mac"]
	    print('mac')
	    print(mac)
	    for i in mac:
		print(i)
	        os.remove('/var/lib/tftpboot/%s'%i)	



        #唤醒瘦客户机
        awakeMac = request.form.get('awakesMacData', '')


	if any(awakeMac):
            mac = json.loads(awakeMac)["awakeMac"]

	    #广播地址 数据包发送到本地子网的广播地址（代码中为：172.16.255.255）的UDP端口9即可唤醒该PC
   	    broadcast = commands.getstatusoutput("ifconfig ovirtmgmt | grep 'inet' | awk -F ' ' '{print $6}' ")
	    dest = (broadcast[1], 9)

	    #UDP 
	    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  	    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
	
	    def sendto(r):
	        print('唤醒:' + r)
    		s.sendto(r,dest)

	    #python利用or在列表解析中调用多个函数 http://www.cnblogs.com/gayhub/p/5277919.html
	    [sendto(binascii.unhexlify('FF'*6+r*16 + '00'*6)) for r in mac]

	    s.close()


        #分组管理：添加分组
        add = request.form.get('addGroupData', '')

	print(add)

        if any(add):
	    groupName = json.loads(add)["add-group-data"]['addGroupName']
            remarks = json.loads(add)["add-group-data"]['remarks']
	    print(groupName)
	    print(remarks)
            #db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            #cursor = db.cursor()

	    try:
	        print('insert')
                add_group_sql = "INSERT INTO groupmanage(GROUP_NAME,GROUP_REMARK) VALUE ('%s','%s') "%(groupName,remarks)
	        print(add_group_sql)
	        cursor.execute(add_group_sql)
	        db.commit()
	    except:
	        print('wrong')
	        db.rollback()

        #分组管理：更改信息
        update = request.form.get('updateGroupData', '')

        print(update)

        if any(update):
            selectGroupName = json.loads(update)["selectGroup"][0]
	    newGroupName = json.loads(update)["update-group-data"]['groupName']
            remarks = json.loads(update)["update-group-data"]['remarks']
            
	    print(selectGroupName)
	    print(newGroupName)
            print(remarks)
            #db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            #cursor = db.cursor()

            try:
                print('update')
                update_group_sql = "UPDATE groupmanage SET GROUP_NAME='%s',GROUP_REMARK='%s' WHERE GROUP_NAME='%s' "%(newGroupName,remarks,selectGroupName)
                print(update_group_sql)
                cursor.execute(update_group_sql)
                db.commit()
            except:
                print('wrong')
                db.rollback()


        #分组管理：删除分组
        delGroup = request.form.get('delGroupData', '')

	if any(delGroup):
            #db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            #cursor = db.cursor()

            groups = json.loads(delGroup)["delGroups"]

            for i in groups:
                try:
                    cursor.execute("DELETE FROM groupmanage WHERE GROUP_NAME='%s' "%(i))
	            #重置对应的终端机的分组属性
		    cursor.execute("UPDATE assets SET CLIENT_GROUP=' ' WHERE CLIENT_GROUP='%s' "%(i)) #语句中不能用双引号
                    db.commit()
                except:
                    db.rollback()

        #唤醒分组
        awakeGroup = request.form.get('awakesGroupData', '')


        if any(awakeGroup):

            #广播地址 数据包发送到本地子网的广播地址（代码中为：172.16.255.255）的UDP端口9即可唤醒
            broadcast = commands.getstatusoutput("ifconfig ovirtmgmt | grep 'inet' | awk -F ' ' '{print $6}' ")
            dest = (broadcast[1], 9)

	    #UDP 
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

            def sendto(r):
                s.sendto(r,dest)

            group = json.loads(awakeGroup)["awakeGroup"]

	    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            cursor = db.cursor()

	    for i in group:
		print(i)
                try:
                    cursor.execute("SELECT CLIENT_MAC FROM assets WHERE CLIENT_GROUP='%s' "%(i))

        	    data = cursor.fetchall()

        	    awake_group = []
        	    for n, row in enumerate(data):
			awake_group.append(row[0])

		    for group in awake_group:
			print('唤醒:' + group)
            		sendto(binascii.unhexlify('FF'*6+group*16 +'00'*6))
            		s.close()

                except:
                    db.rollback()

        backup = request.form.get('backup','')

	print(backup)
	if backup == "backup":
	    os.popen("mysqldump -uroot  -p'%s' ovirt_development assets groupmanage > %s/app/static/data/sql/assets.sql"%("uroot012",os.getcwd()))	

	print('上传资信息')

	file = request.files['file']
        if file:
	    print(file.filename)
            filename = secure_filename(file.filename)
	    filename = gen_file_name(filename)
	    print('filename:')
	    print(filename)
            mimetype = file.content_type
	
	    if not allowed_file(file.filename):

                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="不支持的文件类型")
            	print("文件类型不支持")
	    else:
		uploaded_file_path = os.path.join("%s/app/static/data/uploadsql"%os.getcwd(), filename)
		print(uploaded_file_path)
		os.popen("rm -rf %s/app/static/data/uploadsql/*"%os.getcwd())
		
		file.save(uploaded_file_path)
		print('save')
		
		files = os.listdir("%s/app/static/data/uploadsql"%os.getcwd())
		print(files)
		os.popen("mysql -uroot  -p'%s' ovirt_development < %s/app/static/data/uploadsql/%s"%("uroot012",os.getcwd(),files[0]))
	
		
    return render_template('index/remote.html')

import csv

@main.route('/terminal/return_message', methods=['GET', 'POST'])
@login_required
def terminal_message():

    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
    cursor = db.cursor()

    search_sql =  "SELECT * FROM  assets ORDER BY CLIENT_NAME"

    try:
        cursor.execute(search_sql)
        data = cursor.fetchall()

        jsonData = []
        for n, row in enumerate(data):
            result = {}
            result['CLIENT_MAC'] = row[0]
            result['CLIENT_VNCPWD'] = row[1]
            result['CLIENT_CFGPWD'] = row[2]
            result['CLIENT_DFAPP'] = row[3]
            result['LIENT_DFSRV'] = row[4]
            result['CLIENT_MEM'] = row[5]
	    result['CLIENT_GPU'] = row[6]
	    result['CLIENT_CPU'] = row[7]
	    result['CLIENT_NIC'] = row[8]
            result['CLIENT_OS'] = row[9]
	    result['CLIENT_Model'] = row[10]
      	    result['CLIENT_STORAGE'] = row[11]
	    result['CLIENT_KERNEL'] = row[12]
	    result['CLIENT_IP'] = row[13]
            result['CLIENT_AUDIO'] = row[14]
  	    result['CLIENT_VERSION'] = row[15]
	    result['CLIENT_NAME'] = row[16]
	    result['CLIENT_FREQ'] = row[17]
 	    result['CLIENT_DISPLAY'] = row[18]
	    result['CLIENT_OPT'] = row[19]
	    result['CLIENT_SESSION_0_TYPE'] = row[20]
	    result['CLIENT_LANGUAGE'] = row[21]
	    result['CLIENT_GROUP'] = row[22]

            jsonData.append(result)

	csvData = []
	for row in data:
	    csvData.append(row)

	filename = '%s/app/static/assets.csv'%os.getcwd()
	csvfile = file(filename,'wb')

	writer = csv.writer(csvfile)
	writer.writerow(["CLIENT_MAC","CLIENT_VNCPWD","CLIENT_CFGPWD","CLIENT_DFAPP","CLIENT_DFSRV","CLIENT_MEM","CLIENT_GPU","CLIENT_CPU","CLIENT_NIC","CLIENT_OS","CLIENT_Model","CLIENT_STORAGE","CLIENT_KERNEL","CLIENT_IP","CLIENT_AUDIO","CLIENT_VERSION","CLIENT_NAME","CLIENT_FREQ","CLIENT_DISPLAY","CLIENT_OPT","CLIENT_SESSION_0_TYPE","CLIENT_LANGUAGE"])
	data = csvData
	writer.writerows(csvData)
	csvfile.close()


        return json.dumps(jsonData)
    except:
        db.rollback()

    db.close()


@main.route('/check_message', methods=['GET', 'POST'])
@login_required
def check_message():

    get_mac = request.form.get('mac_data','')
    mac = json.loads(get_mac)["mac"]

    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
    cursor = db.cursor()

    search_sql =  "SELECT * from assets where CLIENT_MAC='%s'"%mac
    try:
        cursor.execute(search_sql)
        data = cursor.fetchall()


        jsonData = []
        for n, row in enumerate(data):
            CLIENT_MAC = row[0]
            CLIENT_VNCPWD = row[1]
            CLIENT_CFGPWD = row[2]
            CLIENT_DFAPP = row[3]
            CLIENT_DFSRV = row[4]
            CLIENT_MEM = row[5]
            CLIENT_GPU = row[6]
            CLIENT_CPU = row[7]
            CLIENT_NIC = row[8]
            CLIENT_OS = row[9]
            CLIENT_Model = row[10]
            CLIENT_STORAGE = row[11]
            CLIENT_KERNEL = row[12]
            CLIENT_IP = row[13]
            CLIENT_AUDIO = row[14]
            CLIENT_VERSION = row[15]
            CLIENT_NAME = row[16]
            CLIENT_FREQ = row[17]
            CLIENT_DISPLA = row[18]
            CLIENT_OPT = row[19]
            CLIENT_SESSION_0_TYPE= row[20]
            CLIENT_LANGUAGE = row[21]


            #result = {}
            #result['CLIENT_MAC'] = row[0]
            #result['CLIENT_VNCPWD'] = row[1]
            #result['CLIENT_CFGPWD'] = row[2]
            #result['CLIENT_DFAPP'] = row[3]
            #result['CLIENT_DFSRV'] = row[4]
            #result['CLIENT_MEM'] = row[5]
            #result['CLIENT_GPU'] = row[6]
            #result['CLIENT_CPU'] = row[7]
            #result['CLIENT_NIC'] = row[8]
            #result['CLIENT_OS'] = row[9]
            #result['CLIENT_Model'] = row[10]
            #result['CLIENT_STORAGE'] = row[11]
            #result['CLIENT_KERNEL'] = row[12]
            #result['CLIENT_IP'] = row[13]
            #result['CLIENT_AUDIO'] = row[14]
            #result['CLIENT_VERSION'] = row[15]
            #result['CLIENT_NAME'] = row[16]
            #result['CLIENT_FREQ'] = row[17]
            #result['CLIENT_DISPLAY'] = row[18]
            #result['CLIENT_OPT'] = row[19]
            #result['CLIENT_SESSION_0_TYPE'] = row[20]
            #result['CLIENT_LANGUAGE'] = row[21]

            #jsonData.append(result)

        return simplejson.dumps({"CLIENT_MAC": row[0],"CLIENT_VNCPWD":row[1],"CLIENT_CFGPWD":row[2],"CLIENT_DFAPP":row[3],"CLIENT_DFSRV":row[4],"CLIENT_MEM":row[5],"CLIENT_GPU":row[6],"CLIENT_CPU":row[7],"CLIENT_NIC":row[8],"CLIENT_OS":row[9],"CLIENT_Model":row[10],"CLIENT_STORAGE":row[11],"CLIENT_KERNEL":row[12],"CLIENT_IP":row[13],"CLIENT_AUDIO":row[14],"CLIENT_VERSION":row[15],"CLIENT_NAME":row[16],"CLIENT_FREQ":row[17],"CLIENT_DISPLAY":row[18],"CLIENT_OPT":row[19],"CLIENT_SESSION_0_TYPE":row[20],"CLIENT_LANGUAGE":row[21]})

    except:
        db.rollback()

    db.close()


#分组信息返回
@main.route('/client_group/return_message', methods=['GET', 'POST'])
@login_required
def client_group_message():
    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
    cursor = db.cursor()

    search_sql =  "SELECT * FROM  groupmanage ORDER BY GROUP_NAME"

    try:
        cursor.execute(search_sql)
        data = cursor.fetchall()

        jsonData = []
        for n, row in enumerate(data):
            result = {}
            result['GROUP_NAME'] = row[0]
            result['GROUP_REMARK'] = row[1]

            jsonData.append(result)


        return json.dumps(jsonData)
    except:
        db.rollback()

    db.close()

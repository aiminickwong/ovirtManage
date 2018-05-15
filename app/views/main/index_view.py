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




@main.route('/system',methods=['GET','POST'])
@login_required
def system():
    if request.method == 'POST':
	data_shutdown = request.form.get('system_shutdown', '')
        #any判断一个对象是否为空的方法
        if  any(data_shutdown):
            try:
                is_shutdown=json.loads(data_shutdown)["is-shutdown"]
                if is_shutdown =='shutdown':
                    message = commands.getstatusoutput('shutdown -h now')
                return simplejson.dumps({"message": message})
            except:
                print 'None'

        data_reboot = request.form.get('system_reboot', '')
        #any判断一个对象是否为空的方法
        if  any(data_reboot):
            try:
                is_reboot=json.loads(data_reboot)["is-reboot"]
                if is_reboot =='reboot':
                    message = commands.getstatusoutput('reboot')
	
                return simplejson.dumps({"message": message})
            except:
                print 'None'



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

ALLOWED_EXTENSIONS = set(['iso','txt','sql', 'gz'])
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
        file = request.files['file']
        if fet-pwdle:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):

                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="不支持的文件类型")


            else:
                # save file to disk  os.getcwd()获取当前脚本路径
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # 在saving后保存上传日期和路径
                # 获取系统时间
                #get_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
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
	#with open("vnc/noVNC/vnc_lite.html",'r') as f:
    	    #htmlstr = f.read()

	#获取终端密码
	get_vnc_pwd = request.form.get('vnc_pwd_data','')
	vnc_pwd = json.loads(get_vnc_pwd)["pwd"]
	#html_output = re.sub(r'<input type=password size=10 id="password_input" class="noVNC_status" value="\w+">',r'<input type=password size=10 id="password_input" class="noVNC_status" value="%s">'%(vnc_pwd),htmlstr)

        #with open("vnc/noVNC/vnc_lite.html",'w') as fw:
    	    #fw.write(html_output)

	# 只需要修改rfb.js中的密码
  	with open("vnc/noVNC/core/rfb.js",'r') as f:
	    jsstr = f.read()

	js_output = re.sub(r'this._rfb_password = "\w+";','this._rfb_password = "%s";'%(vnc_pwd),jsstr)

	with open("vnc/noVNC/core/rfb.js",'w') as fw:
	    fw.write(js_output)

    novnc_pwd()

    return simplejson.dumps({"server_ip": server_ip})


@main.route('/remote', methods=['GET', 'POST'])
@login_required
def remote():

    # 后台自动扫描终端机 与服务器一致的网段
    scan_ip = commands.getstatusoutput("ifconfig ovirtmgmt | grep 'inet' | awk -F ' ' '{print $2}' ")
    #print('scan_ip', scan_ip[1].split('\n')[0].split('.'))
    ip1 = scan_ip[1].split('\n')[0].split('.')[0]
    ip2 =  scan_ip[1].split('\n')[0].split('.')[1]
    ip3 = scan_ip[1].split('\n')[0].split('.')[2]

    for i in range(1,255):
        auto_search = os.popen('tcmclient  %s.%s.%s.%s --scani&'%(ip1,ip2,'129',i))


    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
    cursor = db.cursor()

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
            else:
                sql = insert_sql

            return sql

    '''
        函数说明:执行sql操作
    '''
    def db_execute(sql):
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    def search_file():
        filenames = os.listdir('/var/lib/tftpboot/asset')
        if filenames != " ":
            for filename in filenames:
                sql_lines = read_file('/var/lib/tftpboot/asset/%s'%filename)
                db_execute(sql_lines)

    def write_vnc_tokens():
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

    search_file()
    write_vnc_tokens()


    if request.method == 'POST':
        db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
        cursor = db.cursor()      

	#若不存在，生成资产表
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

	#搜索终端ip
	re_data = request.form.get('data', '')
        if any(re_data):
            try:
                form_data = json.loads(re_data)["data"]
                ipaddr_1 = form_data['ipaddr_1']
	        ipaddr_2 = form_data['ipaddr_2']
	        ipaddr_3 = form_data['ipaddr_3']

                if ipaddr_1 and ipaddr_2 and ipaddr_3 != "":
		    def search_task():
                        for i in range(1,255):
			    #这里不用commands命令,会出现问题
   		            search = os.popen('tcmclient  %s.%s.%s.%s --scani&'%(ipaddr_1,ipaddr_2,ipaddr_3,i))

	        search_task()

            except Exception as e:
               print e

            search_file()
	    write_vnc_tokens()

	#加入到分组
	add_to_group_users = request.form.get('users_data', '')
	if any(add_to_group_users):
	    groupName =  json.loads(add_to_group_users)["selected_group"]
	    select_users = json.loads(add_to_group_users)["select_users"]
            for i in select_users:
	        try:
	            cursor.execute("UPDATE assets SET CLIENT_GROUP='%s' WHERE CLIENT_NAME='%s' "%(groupName,i))
	            db.commit()
	        except Exception, e:
		    print(e)

		    db.rollback()


        #移出分组
        add_remove_group_users = request.form.get('remove_users_from_group_data', '')
        if any(add_remove_group_users):
            select_users = json.loads(add_remove_group_users)["selected_users"]
            for i in select_users:
		print('i',i)
                try:
                    cursor.execute("UPDATE assets SET CLIENT_GROUP='' WHERE CLIENT_NAME='%s' "%(i))
                    db.commit()
                except Exception, e:
                    print(e)

                    db.rollback()



	#删除瘦客户机
	del_users = request.form.get('del_users', '')
        if any(del_users):
	    macs = json.loads(del_users)["select_mac"]
	    for i in macs:
	  	print('macmac', i)
                try:
                    cursor.execute("DELETE FROM assets WHERE CLIENT_MAC='%s' "%(i))
                    db.commit()
                except:
                    db.rollback()

	    #删除对应的瘦客户机文本文件
	    mac = json.loads(del_users)["select_mac"]
	    try:
	        for i in mac:
	            os.remove('/var/lib/tftpboot/asset/%s'%i)
	    except Exception,e:
	        print('文件已删除')

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

        #重启瘦客户机
        rebootIp = request.form.get('rebootIpData', '')
        if any(rebootIp):
            ip = json.loads(rebootIp)["rebootIp"]
	    [os.popen('tcmclient  %s --rebooti&'%(i)) for i in ip]


        #关闭瘦客户机
        shutdownIp = request.form.get('shutdownIpData', '')
        if any(shutdownIp):
            ip = json.loads(shutdownIp)["shutdownIp"]
	    [os.popen('tcmclient  %s --shutdowni&'%(i)) for i in ip]
	    #shut = os.popen('tcmclient  %s --shutdowni&'%(ip[0]))


        #上传瘦客户机配置
        upload_ip = request.form.get('uploadIpData', '')
        if any(upload_ip):
            ip = json.loads(upload_ip)["uploadIp"]
	    upload_config =  os.popen('tcmclient  %s --upconfig'%(ip[0]))
	    upload_result  = upload_config.readlines()
	    file_path = '/var/lib/tftpboot/xConfig'
	    if upload_result[0] == 'true\n':
                config_files = os.listdir(file_path)
	        for con in config_files:
		    if 'tar' in con:
		        # 返回的文件名是否已存在xconfigs表中
	                try:
                            cursor.execute("INSERT IGNORE INTO xconfigs(CONFIG_NAME,CONFIG_REMARK) VALUES('%s','')"%(con))
                            db.commit()
                        except Exception,e:
			    print e
                            db.rollback()

	                    # 保存命令运行后的结果
		        # '复制文件到static目录下'
			os.popen("cp %s/%s %s/app/static/data/profiles/"%(file_path, con, os.getcwd()))           
                        
                return simplejson.dumps({"upconfig_result":"succeed"})
            else:
                return simplejson.dumps({"upconfig_result":"failed"})
	
	#分发瘦客户机配置
	down_ip = request.form.get('sub_config_data', '')
        if any(down_ip):
            config = json.loads(down_ip)["submit_config"]
	    ip = json.loads(down_ip)["submit_ip"]

	    write_ixconfig = config.split('-')[0]
	    if write_ixconfig == "ixConfig":
	        split_by = config.split('.', 1)
		to_xconfig = split_by[0].split('ix', 1)
		# 把分发配置文件写入ixConfig	        
	        with open('/var/lib/tftpboot/xConfig/ixConfig', 'w') as f:
 		    f.write(to_xconfig[1])
	    else:
                split_by = config.split('.', 1)
                to_xconfig = split_by[0].split('vx', 1)
                # 把分发配置文件写入ixConfig            
                with open('/var/lib/tftpboot/xConfig/vxConfig', 'w') as f:
                    f.write(to_xconfig[1])

	    # 执行tcmclient分发命令
	    for i in ip:
	        os.popen('tcmclient  %s --downconfig'%(i))
	    
            # 保存命令运行后的结果
            #down_result = []
            #for line in down_config.readlines():
            #down_result.append(line)
	
	
	#分组管理：添加分组
        add = request.form.get('addGroupData', '')
        if any(add):
	    groupName = json.loads(add)["add-group-data"]['addGroupName']
            remarks = json.loads(add)["add-group-data"]['remarks']

	    try:
                add_group_sql = "INSERT INTO groupmanage(GROUP_NAME,GROUP_REMARK) VALUE ('%s','%s') "%(groupName,remarks)
	        cursor.execute(add_group_sql)
	        db.commit()
	    except:
	        print('wrong')
	        db.rollback()

        #分组管理：更改信息
        update = request.form.get('updateGroupData', '')
        if any(update):
            selectGroupName = json.loads(update)["selectGroup"][0]
	    newGroupName = json.loads(update)["update-group-data"]['groupName']
            remarks = json.loads(update)["update-group-data"]['remarks']
            
            #db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
            #cursor = db.cursor()

            try:
                update_group_sql = "UPDATE groupmanage SET GROUP_NAME='%s',GROUP_REMARK='%s' WHERE GROUP_NAME='%s' "%(newGroupName,remarks,selectGroupName)
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
            #广播地址 数据包发送到本地子网的广播地址（代码中为：172.16.128.255）的UDP端口9即可唤醒
            broadcast = commands.getstatusoutput("ifconfig ovirtmgmt | grep 'inet' | awk -F ' ' '{print $6}' ")
            dest = (broadcast[1], 9)

	    #UDP 
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

            def sendto(r):
                s.sendto(r,dest)

            group = json.loads(awakeGroup)["awakeGroup"]

	    for i in group:
                try:
                    cursor.execute("SELECT CLIENT_MAC FROM assets WHERE CLIENT_GROUP='%s' "%(i))

        	    data = cursor.fetchall()

        	    awake_group = []
        	    for n, row in enumerate(data):
			awake_group.append(row[0])

		    for g in awake_group:
			print('唤醒:' + g)
            		sendto(binascii.unhexlify('FF'*6+g*16 +'00'*6))
            		s.close()

                except:
                    db.rollback()
	
        #重启分组
        rebootGroup = request.form.get('rebootGroupData', '')
        if any(rebootGroup):
            groups = json.loads(rebootGroup)["rebootGroup"]
            for group in groups:
                try:
                    cursor.execute("SELECT CLIENT_IP FROM assets WHERE CLIENT_GROUP='%s' "%(group))

                    data = cursor.fetchall()

                    reboot_group = []
                    for n, row in enumerate(data):
                        reboot_group.append(row[0])

                    [os.popen('tcmclient  %s --rebooti&'%(ip)) for ip in reboot_group]
                except:
                    db.rollback()


        #关闭分组
        shutdownGroup = request.form.get('shutdownGroupData', '')
        if any(shutdownGroup):
	    groups = json.loads(shutdownGroup)["shutdownGroup"]
	    for group in groups:
	        try:
                    cursor.execute("SELECT CLIENT_IP FROM assets WHERE CLIENT_GROUP='%s' "%(group))

                    data = cursor.fetchall()

                    shutdown_group = []
                    for n, row in enumerate(data):
                        shutdown_group.append(row[0])

                    [os.popen('tcmclient  %s --shutdowni&'%(ip)) for ip in shutdown_group]	
                    #for ip  in shutdown_group:
                except:
                    db.rollback()


        # 为组分发配置
        downconfigGroup = request.form.get('sub_config_group_data', '')
        if any(downconfigGroup):
            group_config = json.loads(downconfigGroup)["submit_group_config"]
	    group_name = json.loads(downconfigGroup)["submit_group"]
	    write_ixconfig = group_config.split('-')[0]
            if write_ixconfig == "ixConfig":
                split_by = group_config.split('.', 1)
                to_xconfig = split_by[0].split('ix', 1)
                # 把分发配置文件写入ixConfig            
                with open('/var/lib/tftpboot/xConfig/ixConfig', 'w') as f:
                    f.write(to_xconfig[1])
            else:
                split_by = group_config.split('.', 1)
                to_xconfig = split_by[0].split('vx', 1)
                # 把分发配置文件写入ixConfig            
                with open('/var/lib/tftpboot/xConfig/vxConfig', 'w') as f:
                    f.write(to_xconfig[1])

   	    for group in group_name:
                try:
                    cursor.execute("SELECT CLIENT_IP FROM assets WHERE CLIENT_GROUP='%s' "%(group))

                    data = cursor.fetchall()

                    downconfig_group = []
                    for n, row in enumerate(data):
                        downconfig_group.append(row[0])

                    [os.popen('tcmclient  %s --downconfigi&'%(ip)) for ip in downconfig_group]
                    for ip  in downconfig_group:
                        print(' 分发配置:' + ip)
                except:
                    db.rollback()

	#备份资产信息
	backup = request.form.get('backup','')

	if backup == "backup":
	    os.popen("mysqldump -uroot  -p'%s' ovirt_development assets groupmanage > %s/app/static/data/sql/assets.sql"%("uroot012",os.getcwd()))	

	# !!!!!!!!  这里出了400问题！！# !!!!!!!!
	#file = request.values.get("form_data")
	try:
	    file=request.files['assetfile']

            if file:
                print('上传资产信息')
                filename = gen_file_name(file.filename)
                mimetype = file.content_type

                if not allowed_file(file.filename):
                    result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="不支持的文件类型")
                    print("文件类型不支持")
                else:
                    uploaded_file_path = os.path.join("%s/app/static/data/uploadsql"%os.getcwd(), filename)
                    os.popen("rm -rf %s/app/static/data/uploadsql/*"%os.getcwd())
                    file.save(uploaded_file_path)

                    files = os.listdir("%s/app/static/data/uploadsql"%os.getcwd())
                    os.popen("mysql -uroot  -p'%s' ovirt_development < %s/app/static/data/uploadsql/%s"%("uroot012",os.getcwd(),files[0]))

        except Exception,e:
	    print(e)

	# 导入配置文件

        try:
            profile=request.files['profile']

            if profile:
                print('导入配置文件')
                filename = gen_file_name(profile.filename)
                mimetype = profile.content_type

                if not allowed_file(profile.filename):
                    result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="不支持的文件类型")
                    print("文件类型不支持")
                else:
                    uploaded_file_path = os.path.join("%s/app/static/data/profiles"%os.getcwd(), filename)
                    profile.save(uploaded_file_path)
		    uploaded_file_path_local = "/var/lib/tftpboot/xConfig/%s"%filename
		    profile.save(uploaded_file_path_local)

                    config_files = os.listdir("/var/lib/tftpboot/xConfig/")
                    for con in config_files:
                        if 'tar' in con:
                            # 返回的文件名是否已存在xconfigs表中
                            try:
                                cursor.execute("INSERT IGNORE INTO xconfigs(CONFIG_NAME,CONFIG_REMARK) VALUES('%s','')"%(con))
                                db.commit()
                            except Exception,e:
                                print e
                                db.rollback()

        except Exception,e:
            print(e)


	# 修改配置文件备注
	config_name = request.form.get('config_row[CONFIG_NAME]', '')
	config_remark = request.form.get('config_row[CONFIG_REMARK]', '')
	if config_name != "":
	    try:
                cursor.execute("UPDATE xconfigs set CONFIG_REMARK='%s' where CONFIG_NAME='%s'"%(config_remark,config_name))
                db.commit()
            except Exception,e:
                print e
                db.rollback()

	# 删除配置文件
        delconfigGroup = request.form.get('delConfigData', '')
        if any(delconfigGroup):
           configs = json.loads(delconfigGroup)["delConfig"]
	   for conf in configs:
	       # 删除数据表
               try:
                   cursor.execute("DELETE FROM  xconfigs WHERE CONFIG_NAME='%s'"%(conf))
                   db.commit()
               except Exception,e:
                   print e
                   db.rollback()
	       # 删除对应文件
	       file_path = '/var/lib/tftpboot/xConfig/'
	       delconfig = os.popen('rm -rf  %s/%s'%(file_path,conf))
               os.popen('rm -rf  %s/app/static/data/profiles/%s'%(os.getcwd(),conf))
  
	


        # 最后再关闭
        db.close()			
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

            # 检测是否在线
            # online = os.popen('fping %s'%(row[13]))
            #CLIENT_STATUS = []
            #for line in online.readlines():
                #if 'alive' in line:
                    #CLIENT_STATUS.append('在线')
                #else:
                    #CLIENT_STATUS.append('不在线')
 
            #print('CLIENT_STATUS',row[13],CLIENT_STATUS)
            #result['CLIENT_STATUS'] = CLIENT_STATUS[0]


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


#返回配置文件
@main.route('/remote/return_configs', methods=['GET', 'POST'])
@login_required
def configs_message():
    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
    cursor = db.cursor()

    search_sql =  "SELECT * FROM  xconfigs"

    try:
        cursor.execute(search_sql)
        data = cursor.fetchall()

        jsonData = []
        for n, row in enumerate(data):
            result = {}
            result['CONFIG_NAME'] = row[0]
            result['CONFIG_REMARK'] = row[1]

            jsonData.append(result)


        return json.dumps(jsonData)
    except:
        db.rollback()

    db.close()


#返回要分发的配置文件
@main.route('/configs_load_return_json', methods=['GET', 'POST'])
@login_required
def configs_down():
    db = MySQLdb.connect('localhost','root','uroot012','ovirt_development',charset='utf8')
    cursor = db.cursor()

    search_sql =  "SELECT * FROM  xconfigs"

    try:
        cursor.execute(search_sql)
        data = cursor.fetchall()

        jsonData = []
        for n, row in enumerate(data):
            result = {}
            result['text'] = row[0] + ';' +row[1]
            result['id'] = n

            jsonData.append(result)


        return json.dumps(jsonData)
    except:
        db.rollback()

    db.close()


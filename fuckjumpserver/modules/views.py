#__author__:"jcm"

from models import models
from conf import settings
from modules.utils import  print_err
from modules.utils import yaml_parser
from modules.db_conn import engine,session
from modules import ssh_login
from modules import common_filters
import socket

def log_recording(user_obj,bind_host_obj,logs):
    '''
    flush user operations on remote host into DB
    :param user_obj:
    :param bind_host_obj:
    :param logs: list format [logItem1,logItem2,...]
    :return:
    '''
    # print("\033[41;1m--logs:\033[0m",logs)

    session.add_all(logs)
    session.commit()

#同步数据库
def syncdb(argvs):
    print("Syncing DB....")
    #连接数据库 echo=True打印日志
    # engine = models.create_engine(settings.ConnParams,echo=True)

    # 创建所有表结构,engine在db_conn中已经定义
    models.Base.metadata.create_all(engine)

#将主机信息导入到主机表
def create_hosts(argvs):
    '''
    create hosts
    :param argvs:
    :return:
    '''
    if '-f' in argvs and (argvs.index("-f") +1) < len(argvs) :
        #如果 -f 在参数中，获取-f 索引后面的参数，
        hosts_file  = argvs[argvs.index("-f") +1 ]

    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new hosts file>",quit=True)

    source = yaml_parser(hosts_file)

    if source:
        for key,val in source.items():
            #将解析到的yaml文件，将信息复制给Host表中对应的
            obj = models.Host(hostname=key,ip=val.get('ip'), port=val.get('port') or 22)
            #将数据对象添加到session中
            session.add(obj)
        #提交，创建数据
        session.commit()
#将远程主机用户名密码导入到remoteuser表
def create_remoteusers(argvs):
    '''
    create remoteusers
    :param argvs:
    :return:
    '''
    if '-f' in argvs and argvs:
        remoteusers_file  = argvs[argvs.index("-f") +1]
    else:
        print_err("invalid usage, should be:\ncreate_remoteusers -f <the new remoteusers file>",quit=True)
    source = yaml_parser(remoteusers_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj = models.RemoteUser(username=val.get('username'),auth_type=val.get('auth_type'),password=val.get('password'))
            session.add(obj)
        session.commit()
#将访问用户信息导入到user_profile表中
def create_users(argvs):
    '''
    create little_finger access user
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        user_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreateusers -f <the new users file>",quit=True)

    source = yaml_parser(user_file)
    if source:
        for key,val in source.items():
            print(key,val)
            #将yaml文件中获取的信息依次添加到user表中
            obj = models.UserProfile(username=key,password=val.get('password'))
            # if val.get('groups'):
                  #判断yaml中的是否有组名存在于HostGroup表中，并将结果赋值给groups
            #     groups = session.query(models.HostGroup).filter(models.HostGroup.name.in_(val.get('groups'))).all()

                  #yaml中的所有组名都不在HostGroup表中则报错并结束程序
            #     if not groups:
            #         print_err("none of [%s] exist in group table." % val.get('groups'),quit=True)
                  #如果存在将组名列表group
            #     obj.host_groups = groups
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            #print(obj)
            session.add(obj)
        session.commit()
#导入组信息，一个主机可以属于多个组，一个用户可以属于多个组，相反一个组可以有多个主机，一个组可以有多个用户
def create_groups(argvs):
    '''
    create groups
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        group_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreategroups -f <the new groups file>",quit=True)
    source = yaml_parser(group_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj = models.HostGroup(name=key)
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            #
            # if val.get('user_profiles'):
            #     user_profiles = common_filters.user_profiles_filter(val)
            #     obj.user_profiles = user_profiles
            session.add(obj)
        session.commit()
#导入yaml数据到bindhost
def create_bindhosts(argvs):
    '''
    create bind hosts
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        bindhosts_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new bindhosts file>",quit=True)
    source = yaml_parser(bindhosts_file)
    if source:
        for key,val in source.items():
            #print(key,val)
            #查看yaml文件中的主机名是否存在于Host表中，并获取主机对象
            host_obj = session.query(models.Host).filter(models.Host.hostname==val.get('hostname')).first()
            #如果yaml文件中的主机名不在host表中，则抛出异常
            assert host_obj
            for item in val['remote_users']:
                #print(item)
                #判断item中是否有有auth_type,如果没有抛异常并退出
                assert item.get('auth_type')
                #根据auth_type类型，查找与之对应的远程主机用户对象
                if item.get('auth_type') == 'ssh-password':
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username==item.get('username'),
                                                        models.RemoteUser.password==item.get('password')
                                                    ).first()
                else:
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username==item.get('username'),
                                                        models.RemoteUser.auth_type==item.get('auth_type'),
                                                    ).first()
                #如果没有yaml文件中所记录的远程主机对象则报错，并退出
                if not remoteuser_obj:
                    print_err("RemoteUser obj  %s does not exist." % item,quit=True )
                #将主机对象id和远程主机用户名密码对象id 实例化到bindhost对象中
                bindhost_obj = models.BindHost(host_id=host_obj.id,remoteuser_id=remoteuser_obj.id)
                #将数据对象添加到session里
                session.add(bindhost_obj)
                #for groups this host binds to
                #判断读取到的yaml文件中是否有groups 键
                if source[key].get('groups'):
                    #查看Hostgroup中是否有组名存在于yaml文件中获取的groups中
                    group_objs = session.query(models.HostGroup).filter(models.HostGroup.name.in_(source[key].get('groups'))).all()
                    #判断是否存在group对象，没有报错
                    assert group_objs
                    print('groups:', group_objs)
                    #将得到的group_objs对象赋值给bind_host的host_groups变量
                    bindhost_obj.host_groups = group_objs
                #for user_profiles this host binds to
                if source[key].get('user_profiles'):
                    #获取与yaml文件中相同的user对象
                    userprofile_objs = session.query(models.UserProfile).filter(models.UserProfile.username.in_(
                        source[key].get('user_profiles')
                    )).all()
                    #判断use对象
                    assert userprofile_objs
                    print("userprofiles:",userprofile_objs)
                    #将user对象赋值给bindhost
                    bindhost_obj.user_profiles = userprofile_objs
                #print(bindhost_obj)
        session.commit()

#登录认证
def auth():
    '''
    do the user login authentication
    :return:
    '''
    count = 0
    #输入三次密码不正确则退出
    while count <3:
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) ==0:continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) ==0:continue

        user_obj = session.query(models.UserProfile).filter(models.UserProfile.username==username,
                                                            models.UserProfile.password==password).first()
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." %(3-count-1))
            count +=1
    else:
        print_err("too many attempts.")

def welcome_msg(user):
    WELCOME_MSG = '''\033[32;1m
    ------------- Welcome [%s] login fuckjumpserver -------------
    \033[0m'''%  user.username
    print(WELCOME_MSG)


def start_session(argvs):
    print('going to start sesssion ')
    #用户认证
    user = auth()
    if user:
        welcome_msg(user)
        #打印user对象的所有绑定的主机，和所有绑定的主机组
        print(user.bind_hosts)
        print(user.host_groups)
        exit_flag = False
        while not exit_flag:
            if user.bind_hosts:
                #打印只属于user对象没有划分组的主机
                print('\033[32;1mz.\tungroupped hosts (%s)\033[0m' %len(user.bind_hosts) )
            #enumerate(obj) 遍历对象的下标以及对象
            for index,group in enumerate(user.host_groups):
                #打印user.host_groups中的数据，并列出下标，和每个组中的主机个数
                print('\033[32;1m%s.\t%s (%s)\033[0m' %(index,group.name,  len(group.bind_hosts)) )
                # print('%s.\t%s (%s)' %(index,group.name,  len(group.bind_hosts)) )
            #
            choice = input("[%s]:" % user.username).strip()
            if len(choice) == 0:continue

            if choice == 'z':
                print("------ Group: ungroupped hosts ------" )
                #如果输入的是字母‘z’ 则列出与用户绑定的主机用户名，主机名和IP
                for index,bind_host in enumerate(user.bind_hosts):
                    print("  %s.\t%s@%s(%s)"%(index,
                                              bind_host.remote_user.username,
                                              bind_host.host.hostname,
                                              bind_host.host.ip,
                                              ))
                print("----------- END -----------" )
            elif choice.isdigit():
                choice = int(choice)
                if choice < len(user.host_groups):
                    #打印选择的组名
                    print("------ Group: %s ------"  % user.host_groups[choice].name )
                    for index,bind_host in enumerate(user.host_groups[choice].bind_hosts):
                        #打印该组中所有的主机用户名
                        print("  %s.\t%s@%s(%s)"%(index,
                                                  bind_host.remote_user.username,
                                                  bind_host.host.hostname,
                                                  bind_host.host.ip,
                                                  ))
                    print("----------- END -----------" )

                    #host selection
                    while not exit_flag:
                        user_option = input("[(b)back, (q)quit, select host to login]:").strip()
                        if len(user_option)==0:continue
                        if user_option == 'b':break
                        if user_option == 'q':
                            exit_flag = True
                        #判断输入是否位数字字符
                        if user_option.isdigit():
                            user_option = int(user_option)
                            #如果自定义输入小于该用户所属组的绑定的主机的数目
                            if user_option < len(user.host_groups[choice].bind_hosts) :
                                #打印自定义输入所选择的主机信息
                                print('host:',user.host_groups[choice].bind_hosts[user_option])
                                #打印此台机器曾经的日志
                                logs_list = ['%s 登录了 %s ---%s'%(i.user_profile.username,i.bind_host.host.ip,i.date) for i in user.audit_logs if i.user_profile.username==user.username and i. action_type=='login']
                                print('audit log:',logs_list)

                                #调用ssh_login登录此台机器


                                ssh_login.ssh_login(user,
                                                    user.host_groups[choice].bind_hosts[user_option],
                                                    session,
                                                    user.host_groups[choice].bind_hosts[user_option].remote_user.auth_type,
                                                    log_recording)

                else:
                    print("no this option..")

def wrapper(func):
    def authen(*args,**kwargs):
        m = 0
        while True:
            if m >2:
                print('超出次数')
                break
            username = input('username:')
            password = input('password:')
            auth = session.query(models.UserProfile).filter(models.UserProfile.username==username,models.UserProfile.password==password).first()
            if auth:
                return func(username,**kwargs)
            else:
                print('用户名或者密码错误')
                m +=1
                print(m)
    return authen

@wrapper
def log_audit(*args,**kwargs):
    user = args[0]
    while True:
        username = input('[(q)quit  请输入要查询的用户 :]')
        auth = session.query(models.UserProfile).filter(models.UserProfile.username==username).first()
        if auth:
            user_log = auth.audit_logs
            if user_log:
                for i in user_log:
                    if i.action_type == 'login':
                        print('%s 用户使用%s账户登录了%s ------- %s'%(username,i.bind_host.remote_user.username,i.bind_host.host.ip,i.date))
                    elif i.cmd != 'exit':
                        print('%s 用户使用%s账户在%s 执行了[%s] ------- %s'%(username,i.bind_host.remote_user.username,i.bind_host.host.ip,i.cmd,i.date))
                    else:
                        print('%s 用户使用%s账户退出了%s ------- %s' % (
                        username, i.bind_host.remote_user.username, i.bind_host.host.ip,i.date))
        elif username=='q' or username == 'Q':
            break
        else:
            print('输入的用户不正确')




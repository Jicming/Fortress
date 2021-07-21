#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import base64
import getpass
import os
import socket
import sys
import traceback
# from paramiko.py3compat import input
from  models import models
from modules.db_conn import engine,session
import datetime

import paramiko
try:
    import interactive
except ImportError:
    from . import interactive

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
print(BASE_PATH)


def ssh_login(user_obj,bind_host_obj,session,ssh_type,log_recording):
    # now, connect and use paramiko Client to negotiate SSH2 across the connection

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if ssh_type == 'ssh-key':
            print("waite a moment")
            pkey = paramiko.RSAKey.from_private_key_file(BASE_PATH+'\\'+'id_rsa')
            client.connect(bind_host_obj.host.ip,
                           bind_host_obj.host.port,
                           bind_host_obj.remote_user.username,
                           pkey=pkey,
                           timeout=30
                           )
        elif ssh_type == 'ssh-password':
            client.connect(bind_host_obj.host.ip,
                           bind_host_obj.host.port,
                           bind_host_obj.remote_user.username,
                           bind_host_obj.remote_user.password,
                           timeout=30)
        print('*** Connecting...')
        #client.connect(hostname, port, username, password)

        cmd_caches = []
        chan = client.invoke_shell()
        # chan.keep_this = client
        # print(repr(client.get_transport()))
        print('*** Here we go!\n')
        cmd_caches.append(models.AuditLog(user_id=user_obj.id,
                                          bind_host_id=bind_host_obj.id,
                                          action_type='login',
                                          date=datetime.datetime.now()
                                          ))
        log_recording(user_obj,bind_host_obj,cmd_caches)


        try:
            interactive.interactive_shell(chan,user_obj,bind_host_obj,cmd_caches,log_recording)

            chan.close()
            client.close()
        except OSError as e:
            print('用户%s 已经退出 %s 主机 ' % (user_obj.username, bind_host_obj.host.ip))

            chan.close()
            client.close()

    except Exception  as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()

        except:
            pass
        # sys.exit(1)
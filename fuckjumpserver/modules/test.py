#__author__:"jcm"
import os
import paramiko
BASEPATH = os.path.dirname(os.path.abspath(__file__))

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)
pkey = paramiko.RSAKey.from_private_key_file(BASEPATH +'\\' + 'Identity')
ssh.connect('192.168.190.131',22,'root',pkey=pkey)
# paramiko.rsakey.RSAKey
stdin, stdout, stderr = ssh.exec_command('ls')
print(stdout.read().decode())
print(stderr.read())

ssh.close()


# def ssh_scp(ip, port, user):
#     private_key = paramiko.RSAKey.from_private_key_file(BASEPATH +'\\' + 'Identity')
#     # 创建一个SSH客户端对象
#     ssh = paramiko.SSHClient()
#     # 设置访问策略
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     # 创建连接
#     ssh.connect(ip, port, user, pkey=private_key)
#     stdin, stdout, stderr = ssh.exec_command('ls')
#     print(stdout.read().decode())
#     # sftp = ssh.open_sftp()
# ssh_scp('192.168.190.131',22,'root')


























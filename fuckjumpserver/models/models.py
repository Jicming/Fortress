#__author__:"jcm"
from sqlalchemy import  Table,Column,Integer,String,UniqueConstraint,ForeignKey,DateTime

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy_utils import ChoiceType,PasswordType

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


user_m2m_bindhost = Table('user_m2m_bindhost',Base.metadata,
                          Column('userprofile_id',Integer,ForeignKey('user_profile.id')),
                          Column('bindhost_id',Integer,ForeignKey('bind_host.id')))
bindhost_m2m_hostgroup = Table('bindhost_m2m_hostgroup',Base.metadata,
                          Column('bindhost_id',Integer,ForeignKey('bind_host.id')),
                          Column('hostgroup_id',Integer,ForeignKey('host_group.id')))

user_m2m_hostgroup = Table('user_m2m_hostgroup',Base.metadata,
                          Column('userprofile_id',Integer,ForeignKey('user_profile.id')),
                          Column('hostgroup_id',Integer,ForeignKey('host_group.id')))

#主机表
class Host(Base):
    __tablename__='host'
    id =Column(Integer,primary_key=True)
    hostname =Column(String(64),unique=True)
    ip =Column(String(64),unique=True)
    port = Column(Integer,default=22)

    def __repr__(self):
        return self.hostname
#主机组表
class HostGroup(Base):
    __tablename__ = 'host_group'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique=True)
    #绑定与BindHost表的多对多关系，BindHost可以使用host_groups进行反查。
    bind_hosts = relationship('BindHost',secondary='bindhost_m2m_hostgroup',backref='host_groups')
    def __repr__(self):
        return self.name
#远程主机用户表
class RemoteUser(Base):
    __tablename__='remote_user'
    #将auth_type、username、password 设备联合唯一索引，索引名为_user_passwd_uc
    __table_args__=(UniqueConstraint('auth_type','username','password',name='_user_passwd_uc'),)
    AuthTypes = [
        ('ssh-password','SSH/Password'),
        ('ssh-key','SSH/KEY'),
    ]
    id = Column(Integer,primary_key=True)
    auth_type = Column(ChoiceType(AuthTypes))
    username =Column(String(32))
    password = Column(String(128))

    def __repr__(self):
        return self.username
#远程主机和主机用户表，
class BindHost(Base):
    '''
    192.168.1.11 web
    192.168.1.11 mysql
    '''
    __tablename__ = 'bind_host'
    #确保每台主机和密码一一对应，设置主机id（host_id）字段 和用户id（remoteuser_id）字段设备联合唯一
    __table_args__ = (UniqueConstraint('host_id','remoteuser_id',name='_host_remoteuser_uc'),)
    id = Column(Integer,primary_key=True)
    host_id = Column(Integer,ForeignKey('host.id'))
    # group_id = Column(Integer,ForeignKey('group.id'))
    remoteuser_id = Column(Integer,ForeignKey('remote_user.id'))
    #设置Host表的反查
    host = relationship('Host',backref='bind_hosts')
    # group = relationship('HostGroup',backref='bind_hosts')
    #设置remoteuser表使用bind_hosts进行反查
    remote_user = relationship('RemoteUser',backref='bind_hosts')
    def __repr__(self):
        return '<%s -- %s>'%(self.host.ip,self.remote_user.username)
#用户表
class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer,primary_key=True)
    username = Column(String(32),unique=True)
    password = Column(String(128))
    bind_hosts = relationship('BindHost',secondary='user_m2m_bindhost',backref='user_profiles')
    host_groups = relationship('HostGroup',secondary='user_m2m_hostgroup',backref='user_profiles')

class AuditLog(Base):
    __tablename__= 'audit_log'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user_profile.id'))
    bind_host_id = Column(Integer,ForeignKey('bind_host.id'))
    action_choices =[
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'Execption')]
    action_choices2 =[
        (u'cmd',u'CMD'),
        (u'login',u'Login'),
        (u'login',u'Logout'),
    ]
    action_type = Column(ChoiceType(action_choices2))
    cmd = Column(String(255))
    date =Column(DateTime)
    user_profile = relationship('UserProfile',backref='audit_logs')
    bind_host = relationship('BindHost',backref = 'audit_logs')
    #
    # def __repr__(self):
    #     if self.user_profile and self.bind_host and self.date:
    #         return '用户：%s 登录了主机 %s --- %s'%(self.user_profile.username,self.bind_host.host.ip,self.date)





























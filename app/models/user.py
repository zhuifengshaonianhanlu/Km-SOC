#coding:utf-8

"""
Author:hanlu
"""
import uuid,re
from app.models.base import db
from flask_login import UserMixin
from app import login_manager
from sqlalchemy import Column,Integer,String,DateTime
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
    '''
    User类中继承UserMinin,不需要重复定义里面的方法
    user table
    '''
    __tablename__ = 'user'

    id = Column(Integer(),autoincrement=True,primary_key=True)
    ctime = Column(DateTime)
    username = Column(String(64))
    password = Column(String(256))
    email = Column(String(64))
    usertype = Column(Integer())
    uid = Column(String(128))


    def __repr__(self):
        return '<%r,%r,%r,%r,%r,%r,%r>' % (self.id,self.ctime,self.username,self.password,self.email,self.usertype,self.uid)


    #默认范围id,需要重写userminin类中的方法：get_id，修改为uid
    def get_uid(self):
        try:
            return self.uid
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


def get_uid(username):
    return str(uuid.uuid5(uuid.NAMESPACE_OID,username))

#指定login_manager.user_loader装饰器，通过该装饰器获取用户信息，这里的get_user里面的uid是User类中get_id指定的
@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
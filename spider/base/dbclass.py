#coding:utf-8

"""
Author:hanlu

create database newsoc default charset utf8 collate utf8_general_ci;
"""

import pymysql,time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Table,MetaData,ForeignKey,Column,Integer,String,Text,Boolean,Time,Date,DateTime
from sqlalchemy.orm import mapper,sessionmaker

Base = declarative_base()

class Create_result(Base):
    '''
    table for Search result,include keyword and payload
    '''
    __tablename__ = 'kmresult'
    # id = Column(Integer(),autoincrement=True,primary_key=True)
    eventtime = Column(DateTime(),comment='时间')
    owner = Column(String(256),comment='项目作者名称')
    pname = Column(String(256),comment='项目名称')
    purl = Column(Text(),comment='项目地址')
    filename = Column(String(256),comment='文件名')
    filehash = Column(String(256),primary_key=True,comment='文件hash')
    fileurl = Column(Text(),comment='文件url')
    filetype = Column(String(256),comment='文件类型')
    confirm = Column(Boolean(),comment='是否确认')
    source = Column(String(256),comment='来源')
    keyword = Column(String(256),comment='关键字')
    payload = Column(String(256),comment='payload')
    content = Column(Text(),comment='命中的内容base64编码')
    note = Column(Text(),comment='确认时的注释')


class Create_wlist(Base):
    __tablename__ = 'kmwhitelist'
    eventtime = Column(DateTime(),comment='时间')
    owner = Column(String(256), comment='项目作者名称')
    pname = Column(String(256), comment='项目名称')
    purl = Column(String(256), primary_key=True,comment='项目地址')


def merge_result(connect,**kwargs):
    '''
    eventtime, owner, pname, purl, filename, filehash, fileurl, filetype, confirm, source, keyword,payload,content
    :param filehash: 如果文件hash相同，就更新而不是插入
    '''
    Session_class = sessionmaker(bind=connect)
    Session = Session_class()

    confirmis = Session.query(Create_result).filter_by(filehash=kwargs.get('filehash')).all()
    #如果filehash不存在，就插入
    if not confirmis:
        result_obj = Create_result(eventtime=kwargs.get('eventtime'),
                                   owner=kwargs.get('owner'),
                                   pname=kwargs.get('pname'),
                                   purl=kwargs.get('purl'),
                                   filename=kwargs.get('filename'),
                                   filehash=kwargs.get('filehash'),
                                   fileurl=kwargs.get('fileurl'),
                                   filetype=kwargs.get('filetype'),
                                   confirm=kwargs.get('confirm'),
                                   source=kwargs.get('source'),
                                   keyword=kwargs.get('keyword'),
                                   payload=kwargs.get('payload'),
                                   content=kwargs.get('content'),note=kwargs.get('note'))
        Session.merge(result_obj)
        Session.commit()


def get_wlist(connect):
    Session_class = sessionmaker(bind=connect)
    Session = Session_class()
    wlo = Session.query(Create_wlist).all()
    white_projects = []
    for w in wlo:
        projects = w.owner + '/' + w.pname
        white_projects.append(projects)
    return white_projects











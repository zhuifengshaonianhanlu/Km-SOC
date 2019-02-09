#coding:utf-8

"""
Author:hanlu
"""

from app.models.base import db
from sqlalchemy import Column,Integer,String,DateTime,Text,Boolean

class KmResult(db.Model):
    '''
    kmeye result
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

    # __mapper_args__ = {"order_by": pname.desc()}

    def __repr__(self):
        return '<%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r>' % (self.eventtime,self.owner,self.pname,self.purl,self.filename,self.filehash,
                                                                self.fileurl,self.filetype,self.confirm,self.source,self.keyword,self.payload,
                                                                self.content,self.note)
class KmWhitelist(db.Model):
    __tablename__ = 'kmwhitelist'
    # id = Column(Integer(), autoincrement=True, primary_key=True)
    eventtime = Column(DateTime(), comment='时间')
    owner = Column(String(256), comment='项目作者名称')
    pname = Column(String(256), comment='项目名称')
    purl = Column(String(256), primary_key=True,comment='项目地址')

    def __repr__(self):
        return '<%r,%r,%r,%r>' % (self.eventtime,self.owner,self.pname,self.purl)






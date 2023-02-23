# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = Column(String(20), default=None, nullable=False, comment="姓名")
    _password = Column(String(128), comment="登录密码")
    status = Column(Integer, default=1, nullable=False, comment="状态 0:未激活 1:正常 2:被冻结 9:已注销")
    remark = Column(String(100), default=None, nullable=True, comment="备注")
    created_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=True, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), default=None, onupdate=func.now(), nullable=True, comment="更新时间")

    def __init__(self, items):
        Base().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password_set(self, value):
        self._password = generate_password_hash(value)
    
    def password_check(self, user_input):
        return check_password_hash(self._password, user_input)
    
    def __repr__(self):
        return r"用户ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("被冻结" if self.status==2 else ("已注销" if self.status==9 else "异常状态")))
        )

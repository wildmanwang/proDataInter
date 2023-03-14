# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from apps import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    _password = db.Column(db.String(128), comment="登录密码")
    status = db.Column(db.Integer, default=1, nullable=False, comment="状态 0:未激活 1:正常 2:被冻结 9:已注销")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_time = db.Column(db.DateTime, onupdate=datetime.now, nullable=True, comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    # 创建可读属性
    @property
    def password(self):
        return ''
    
    # 创建可写属性 需要先有可用属性，没有的话，通过@property创建
    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)
    
    def password_check(self, user_input):
        return check_password_hash(self._password, user_input)
    
    def __repr__(self):
        return r"用户ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("被冻结" if self.status==2 else ("已注销" if self.status==9 else "异常状态")))
        )


if __name__ == "__main__":
    newUser = User({"name": "San Zhang", "status": 1})
    db.session.add(newUser)
    db.session.commit()

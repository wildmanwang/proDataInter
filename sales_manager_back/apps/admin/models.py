# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from apps import db
from sqlalchemy import text


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    account = db.Column(db.String(20), nullable=False, unique=True, comment="账号")
    nickname = db.Column(db.String(20), nullable=False, comment="昵称")
    sex = db.Column(db.Integer, comment="性别 0:女 1:男")
    _password = db.Column(db.String(128), comment="登录密码")
    mobile = db.Column(db.String(20), nullable=True, comment="手机号")
    email = db.Column(db.String(100), nullable=True, comment="e-mail地址")
    source = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="来源 0:内部员工 1:主动注册 2:第三方引入")
    last_login = db.Column(db.DateTime, comment="最近登录时间")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 2:被冻结 9:已注销")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

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
        return r"用户ID:{id} 昵称:{nickname} 状态:{status}".format(
            id=self.id,
            name=self.nickname,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("被冻结" if self.status==2 else ("已注销" if self.status==9 else "异常状态")))
        )


class SysApp(db.Model):
    __tablename__ = "sysapp"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, unique=True, comment="名称")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"应用ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )

class SysModel(db.Model):
    __tablename__ = "sysmodel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(20), nullable=False, unique=True, comment="名称")
    sysapp = db.Column(db.Integer, nullable=False, comment="所属应用")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"模块ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )


class SysFunction(db.Model):
    __tablename__ = "sysfunction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, unique=True, comment="名称")
    sysmodel = db.Column(db.Integer, nullable=False, comment="所属模块")
    authorizate_flag = db.Column(db.Integer, server_default=text("1"), comment="是否需要授权")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"功能ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )


class SysOperation(db.Model):
    __tablename__ = "sysoperation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, comment="名称")
    sysfunction = db.Column(db.Integer, nullable=False, comment="所属功能")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"权限ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )


class SysRole(db.Model):
    __tablename__ = "sysrole"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, unique=True, comment="名称")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"角色ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )


class SysPermission(db.Model):
    __tablename__ = "syspermission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    sysrole = db.Column(db.Integer, nullable=False, comment="角色")
    sysoperation = db.Column(db.Integer, nullable=False, comment="权限")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"权限ID:{id}".format(
            id=self.id
        )


class SysAuthorization(db.Model):
    __tablename__ = "sysauthorization"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    user = db.Column(db.Integer, nullable=False, comment="用户")
    sysrole = db.Column(db.Integer, nullable=False, comment="角色")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"用户ID:{user} 角色ID:{role}".format(
            user=self.user,
            role=self.sysrole
        )


class Organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(100), nullable=False, unique=True, comment="名称")
    simple_name = db.Column(db.String(20), nullable=False, unique=True, comment="简称")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"组织ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )


class OrganizationFuncs(db.Model):
    __tablename__ = "organizationfuncs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    organization = db.Column(db.Integer, comment="组织")
    fuction = db.Column(db.Integer, comment="功能")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"组织ID:{organization} 功能ID:{fuction}".format(
            organization=self.organization,
            fuction=self.fuction
        )


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, unique=True, comment="名称")
    organization = db.Column(db.Integer, nullable=False, comment="所属组织")
    incharge = db.Column(db.Integer, comment="负责人")
    order_number = db.Column(db.Integer, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:未激活 1:正常 9:失效")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"部门ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status==1 else ("未激活" if self.status==0 else ("失效" if self.status==9 else "异常状态"))
        )


class Staff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, comment="姓名")
    sex = db.Column(db.Integer, comment="性别 0:女 1:男")
    mobile = db.Column(db.String(20), nullable=True, comment="手机号")
    email = db.Column(db.String(100), nullable=True, comment="e-mail地址")
    department = db.Column(db.Integer, nullable=False, comment="所属部门")
    account = db.Column(db.Integer, comment="账号")
    status = db.Column(db.Integer, nullable=False, server_default=text("0"), comment="状态 0:未转正 1:正式 9:已离职")
    remark = db.Column(db.String(100), nullable=True, comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
    
    def __repr__(self):
        return r"员工ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正式" if self.status==1 else ("未转正" if self.status==0 else ("已离职" if self.status==9 else "异常状态"))
        )


if __name__ == "__main__":
    newUser = User({"name": "San Zhang", "status": 1})
    db.session.add(newUser)
    db.session.commit()

# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = Column(String(20), default=None, nullable=False, comment="类别名称")
    order_num = Column(Integer, default=80, nullable=False, comment="排序号")
    status = Column(Integer, default=1, nullable=False, comment="状态 0:无效 1:正常")
    remark = Column(String(100), default=None, nullable=True, comment="备注")
    created_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=True, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), default=None, onupdate=func.now(), nullable=True, comment="更新时间")

    def __init__(self, **items):
        Base.__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return r"类别ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status == 1 else "无效"
        )


class Supplier(Base):
    __tablename__ = "supplier"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = Column(String(50), default=None, nullable=False, comment="供应商名称")
    simple_name = Column(String(20), default=None, nullable=False, comment="简称")
    code = Column(String(20), default=None, nullable=True, comment="代码")
    status = Column(Integer, default=1, nullable=False, comment="状态 0:无效 1:正常")
    remark = Column(String(100), default=None, nullable=True, comment="备注")
    created_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=True, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), default=None, onupdate=func.now(), nullable=True, comment="更新时间")

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return r"类别ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status == 1 else "无效"
        )


class Goods(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    code = Column(String(20), default=None, nullable=True, comment="商品代码")
    name = Column(String(50), default=None, nullable=False, comment="名称")
    category = Column(Integer, nullable=False, comment="类别")
    category_name = Column(String(20), default=None, nullable=False, comment="类别名称")
    supplier = Column(Integer, nullable=False, comment="供应商")
    supplier_name = Column(String(50), default=None, nullable=False, comment="供应商名称")
    model = Column(String(20), default=None, nullable=True, comment="型号")
    image = Column(String(100), default=None, nullable=True, comment="图片")
    order_num = Column(Integer, default=80, nullable=False, comment="排序号")
    status = Column(Integer, default=1, nullable=False, comment="状态 0:无效 1:正常")
    remark = Column(String(100), default=None, nullable=True, comment="备注")
    created_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=True, comment="创建时间")
    updated_time = Column(DateTime(timezone=True), default=None, onupdate=func.now(), nullable=True, comment="更新时间")

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return r"商品ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status == 1 else "无效"
        )

# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from datetime import datetime
from apps import db
from sqlalchemy import text


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(20), nullable=False, comment="类别名称")
    order_num = db.Column(db.Integer, nullable=False, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:无效 1:正常")
    remark = db.Column(db.String(100), comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # Super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return r"类别ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status == 1 else "无效"
        )


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    name = db.Column(db.String(50), nullable=False, comment="供应商名称")
    simple_name = db.Column(db.String(20), nullable=False, comment="简称")
    code = db.Column(db.String(20), comment="代码")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:无效 1:正常")
    remark = db.Column(db.String(100), comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # Super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return r"类别ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status == 1 else "无效"
        )


class Goods(db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键ID")
    code = db.Column(db.String(20), comment="商品代码")
    name = db.Column(db.String(50), nullable=False, comment="名称")
    category = db.Column(db.Integer, nullable=False, comment="类别")
    category_name = db.Column(db.String(20), nullable=False, comment="类别名称")
    supplier = db.Column(db.Integer, nullable=False, comment="供应商")
    supplier_name = db.Column(db.String(50), nullable=False, comment="供应商名称")
    model = db.Column(db.String(20), comment="型号")
    image = db.Column(db.String(100), comment="图片")
    order_num = db.Column(db.Integer, nullable=False, server_default=text("10"), comment="排序号")
    status = db.Column(db.Integer, nullable=False, server_default=text("1"), comment="状态 0:无效 1:正常")
    remark = db.Column(db.String(100), comment="备注")
    created_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    updated_time = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="更新时间")

    def __init__(self, items):
        # Super().__init__()
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])

    def __repr__(self):
        return r"商品ID:{id} 名称:{name} 状态:{status}".format(
            id=self.id,
            name=self.name,
            status="正常" if self.status == 1 else "无效"
        )

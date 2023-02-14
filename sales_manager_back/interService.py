# -*- coding:utf-8 -*-
"""
flask框架实现数据接口服务
数据返回格式：
rtnData = {
    "result":True,                  # 逻辑控制 True/False
    "dataString":"",               # 字符串
    "dataNumber":1,                # 数字
    "info":"",                      # 信息
    "entities": {                   # 表体集
        "bill":[],                   # 销售单
        "billItem":[],               # 销售单
        "billPay":[]                 # 销售单
    }
}
"""
__author__ = "Cliff.wang"
import json
import config
from sqlalchemy import create_engine
sett = config.DevelopmentConfig()

engine = create_engine(sett.DATABASE_URI, echo=True)

from flask import Flask, request, jsonify, session
from admin import admin
from goods import goods
from ormOper import OrmOper

orm = OrmOper(sett)
app = Flask(__name__)
app.config.from_object(sett)
app.register_blueprint(admin)
app.register_blueprint(goods)

@app.route('/hello', methods=['get', 'post'])
def home():
    return "这里是石将军数据服务接口"

@app.route('/test', methods=['get', 'post'])
def test():
    session["username"] = "张三三"
    return session.get("username")

@app.route( '/user/login', methods=['post'])
def user_login():
    """
    登录
    """
    rtn = orm.user_login("0001", "123456")
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)

@app.route( '/user/info', methods=['get'])
def user_info():
    """
    登录
    """
    sToken = request.args.get("token").strip()
    rtn = orm.user_info(sToken)
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)

@app.route( '/user/logout', methods=['post'])
def user_logout():
    """
    登出
    """
    rtn = orm.user_logout()
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)

if __name__ == '__main__':
    app.run(host=app.config["WEB_SERVER_HOST"], port=app.config["WEB_SERVER_PORT"], debug=True)

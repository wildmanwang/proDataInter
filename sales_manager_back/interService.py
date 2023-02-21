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
from sqlalchemy import create_engine
from flask import Flask, request, jsonify, session

import config
sett = config.DevelopmentConfig()

engine = create_engine(sett.DATABASE_URI, echo=True)

from admin import admin
from goods import goods

app = Flask(__name__)
app.config.from_object(sett)
app.register_blueprint(admin, url_prefix='')
app.register_blueprint(goods, url_prefix='/goods')


@app.route('/hello', methods=['get', 'post'])
def home():
    return "这里是石将军数据服务接口"


@app.route('/test', methods=['get', 'post'])
def test():
    session["username"] = "张三三"
    return session.get("username")


if __name__ == '__main__':
    app.run(host=app.config["WEB_SERVER_HOST"], port=app.config["WEB_SERVER_PORT"], debug=True)

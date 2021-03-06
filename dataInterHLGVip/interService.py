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
from flask import Flask, request
from interConfig import Settings
from interData import InterData
from myTools import MyJSONEncoder
# from flask_apscheduler import APScheduler


sett = Settings()
data = InterData(sett)
server = Flask(__name__)


@server.route('/', methods=['get', 'post'])
def home():
    return "这里是云蝶餐饮数据服务接口"


@server.route('/setVIPInfo', methods=['post'])
def setVIPInfo():
    """
    推送会员信息
    """
    rst = {
        "status": 0,
        "message": ""
    }
    try:
        parab = json.loads(request.get_data(as_text=True))
        rst = data.securityVerify(request.headers, parab)
        if rst["status"] != 1:
            raise Exception(rst["message"])
        rst = data.setVIPInfo(parab)
    except Exception as e:
        rst["message"] = "错误：{info}".format(info=str(e))
    return json.dumps(rst, cls=MyJSONEncoder, ensure_ascii=False)


@server.route('/setVIPCode', methods=['post'])
def setVIPCode():
    """
    推送会员动态二维码
    """
    rst = {
        "status": 0,
        "message": ""
    }
    try:
        parab = json.loads(request.get_data(as_text=True))
        rst = data.securityVerify(request.headers, parab)
        if rst["status"] != 1:
            raise Exception(rst["message"])
        rst = data.setVIPCode(parab)
    except Exception as e:
        rst["message"] = "错误：{info}".format(info=str(e))
    return json.dumps(rst, cls=MyJSONEncoder, ensure_ascii=False)


@server.route('/queryBills', methods=['post'])
def queryBills():
    """
    查询会员消费
    """
    rst = {
        "status": 0,
        "message": ""
    }
    try:
        parab = json.loads(request.get_data(as_text=True))
        rst = data.securityVerify(request.headers, parab)
        if rst["status"] != 1:
            raise Exception(rst["message"])
        rst = data.queryBills(parab)
    except Exception as e:
        rst["message"] = "错误：{info}".format(info=str(e))
    return json.dumps(rst, cls=MyJSONEncoder, ensure_ascii=False)


if __name__ == '__main__':
    # scheduler = APScheduler()
    # scheduler.init_app(server)
    # scheduler.start()
    server.run(host=sett.webHost, port=sett.webPort, debug=True)

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

class Config(object):
    # 任务列表
    JOBS = [
        {
            'id': 'jobHandleScore',
            'func': '__main__:handleScore',
            'trigger': 'interval',
            'seconds': 60,
        }
    ]

sett = Settings()
data = InterData(sett)
server = Flask(__name__)
# server.config.from_object(Config())

def handleScore():
    data.handleScore()

@server.route('/', methods=['get', 'post'])
def home():
    return "这里是云蝶餐饮数据服务接口"

@server.route('/queryToken', methods=['get'])
def queryToken():
    """
    查询access token
    """
    rtn = data.queryToken()

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/getToken', methods=['get'])
def getToken():
    """
    从微信端获取access token
    """
    import urllib.request
    import json
    url = r"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx34a7860ad3af92e4&secret=1f2a0d5d4e266673c443f739c3826672"
    response = urllib.request.urlopen(url)
    return response.read().decode()

@server.route('/queryBillList', methods=['get'])
def queryBillList():
    """
    查询单据列表
    """
    lsStatus = request.args.get("status").strip()
    rtn = data.queryBillList(int(lsStatus))

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/callSoundTaking', methods=['get'])
def callSoundTaking():
    """
    呼叫取餐
    """
    lsBill = request.args.get("billNo").strip()
    rtn = data.callSoundTaking(lsBill)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/callWXTaking', methods=['get'])
def callWXTaking():
    """
    公众号取餐通知
    """
    lsBill = request.args.get("billNo").strip()
    rtn = data.callWXTaking(lsBill)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/setVipPhone', methods=['post'])
def setVipPhone():
    """
    设置单据的会员手机号
    """
    lsBill = request.form.get("billNo").strip()
    lsPhone = request.form.get("phoneNumber").strip()
    rtn = data.setVipPhone(lsBill, lsPhone)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/queryMealNumber', methods=['get'])
def queryMealNumber():
    """
    返回订单列表
    订单号、桌台名称、人数、金额、取餐号
    """
    rtn = data.queryMealNumber()

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

if __name__ == '__main__':
    # scheduler = APScheduler()
    # scheduler.init_app(server)
    # scheduler.start()
    server.run(host=sett.webHost, port=sett.webPort, debug=True)
